#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : topology.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy 二维网格 Half-Edge 拓扑数据结构
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

import numpy as np


class HalfEdgeTopology:
    """二维定向面网格的 Half-Edge 拓扑。

    采用 Structure-of-Arrays 存储，每条半边 h 保存：

        origin[h]    起点
        target[h]    终点
        next[h]      当前 Face 内下一条半边
        prev[h]      当前 Face 内上一条半边
        twin[h]      反向半边，边界半边为 -1
        face[h]      所属 Cell / Face
        edge[h]      对应无向全局 Edge ID

    该结构适合 Triangle / Quad / Polygon 等二维面网格，并为：

        - Vertex one-ring 邻域遍历
        - Delaunay / Voronoi 对偶
        - Edge Flip / Split / Collapse
        - Polygon / VEM
        - Remeshing

    提供统一拓扑基础。
    """

    def __init__(
        self,
        origin,
        target,
        next_,
        prev,
        twin,
        face,
        edge,
        face_halfedge,
        vertex_halfedge,
        edges,
    ):
        self.origin = np.asarray(origin, dtype=int)
        self.target = np.asarray(target, dtype=int)
        self.next = np.asarray(next_, dtype=int)
        self.prev = np.asarray(prev, dtype=int)
        self.twin = np.asarray(twin, dtype=int)
        self.face = np.asarray(face, dtype=int)
        self.edge = np.asarray(edge, dtype=int)
        self.face_halfedge = np.asarray(face_halfedge, dtype=int)
        self.vertex_halfedge = np.asarray(vertex_halfedge, dtype=int)
        self.edges = np.asarray(edges, dtype=int)

        self._validate()

    def _validate(self):
        n = len(self.origin)
        arrays = (
            self.target,
            self.next,
            self.prev,
            self.twin,
            self.face,
            self.edge,
        )
        if any(len(a) != n for a in arrays):
            raise ValueError("half-edge arrays must have identical length")

        if n == 0:
            return

        if np.any(self.origin < 0) or np.any(self.target < 0):
            raise ValueError("half-edge vertex indices must be non-negative")
        if np.any((self.next < 0) | (self.next >= n)):
            raise ValueError("invalid half-edge next index")
        if np.any((self.prev < 0) | (self.prev >= n)):
            raise ValueError("invalid half-edge prev index")
        if np.any((self.twin < -1) | (self.twin >= n)):
            raise ValueError("invalid half-edge twin index")

        # next/prev 必须互为逆关系。
        ids = np.arange(n, dtype=int)
        if not np.array_equal(self.prev[self.next], ids):
            raise ValueError("half-edge next/prev relation is inconsistent")

        # twin 必须对称。
        interior = np.flatnonzero(self.twin >= 0)
        if interior.size and not np.array_equal(self.twin[self.twin[interior]], interior):
            raise ValueError("half-edge twin relation is inconsistent")

    @property
    def number_of_halfedges(self):
        return len(self.origin)

    @property
    def number_of_edges(self):
        return len(self.edges)

    @property
    def number_of_faces(self):
        return len(self.face_halfedge)

    @property
    def number_of_vertices(self):
        return len(self.vertex_halfedge)

    def boundary_halfedge_index(self):
        """返回没有 twin 的边界半边。"""
        return np.flatnonzero(self.twin < 0).astype(int)

    def boundary_edge_index(self):
        """返回边界无向 Edge ID。"""
        h = self.boundary_halfedge_index()
        return np.unique(self.edge[h]).astype(int)

    def boundary_vertex_index(self):
        """返回边界顶点 ID。"""
        h = self.boundary_halfedge_index()
        if h.size == 0:
            return np.empty(0, dtype=int)
        return np.unique(np.concatenate([self.origin[h], self.target[h]])).astype(int)

    def face_halfedges(self, face_id):
        """按 Face 局部方向返回组成该 Face 的半边 ID。"""
        face_id = int(face_id)
        start = int(self.face_halfedge[face_id])
        result = []
        h = start
        while True:
            result.append(h)
            h = int(self.next[h])
            if h == start:
                break
            if len(result) > self.number_of_halfedges:
                raise RuntimeError("invalid half-edge face cycle")
        return np.asarray(result, dtype=int)

    def face_vertices(self, face_id):
        """按局部方向返回 Face 顶点 ID。"""
        h = self.face_halfedges(face_id)
        return self.origin[h].copy()

    def vertex_outgoing_halfedges(self, vertex_id):
        """返回以 vertex_id 为起点的所有半边 ID。"""
        vertex_id = int(vertex_id)
        return np.flatnonzero(self.origin == vertex_id).astype(int)

    def vertex_neighbors(self, vertex_id):
        """返回与指定 Vertex 通过 Edge 相连的一环邻居 Vertex。"""
        vertex_id = int(vertex_id)
        outgoing = self.vertex_outgoing_halfedges(vertex_id)
        incoming = np.flatnonzero(self.target == vertex_id).astype(int)

        neighbors = []
        if outgoing.size:
            neighbors.extend(map(int, self.target[outgoing]))
        if incoming.size:
            neighbors.extend(map(int, self.origin[incoming]))
        if not neighbors:
            return np.empty(0, dtype=int)
        return np.unique(np.asarray(neighbors, dtype=int)).astype(int)

    def vertex_faces(self, vertex_id):
        """返回包含指定 Vertex 的 Face ID。"""
        h = self.vertex_outgoing_halfedges(vertex_id)
        if h.size == 0:
            return np.empty(0, dtype=int)
        return np.unique(self.face[h]).astype(int)

    def vertex_faces_ordered(self, vertex_id, points=None):
        """返回围绕 Vertex 的有序一环 Face。

        优先使用 Half-Edge 环遍历；若 Vertex 位于边界，拓扑环为开链，
        可提供 points 使用几何极角稳定排序。
        """
        vertex_id = int(vertex_id)
        outgoing = self.vertex_outgoing_halfedges(vertex_id)
        if outgoing.size == 0:
            return np.empty(0, dtype=int)

        # 内部顶点可以纯拓扑循环：h -> twin(prev(h))。
        if not np.any(self.twin[self.prev[outgoing]] < 0):
            start = int(outgoing[0])
            faces = []
            h = start
            visited = set()
            while h not in visited:
                visited.add(h)
                faces.append(int(self.face[h]))
                hp = int(self.prev[h])
                ht = int(self.twin[hp])
                if ht < 0:
                    break
                h = ht
            if h == start and len(faces) == len(outgoing):
                return np.asarray(faces, dtype=int)

        faces = self.vertex_faces(vertex_id)
        if points is None or faces.size <= 1:
            return faces

        # 边界/open fan：使用 Face 顶点平均中心相对目标 Vertex 的极角排序。
        points = np.asarray(points, dtype=float)
        p = points[vertex_id, :2]
        centers = []
        for f in faces:
            verts = self.face_vertices(int(f))
            centers.append(points[verts, :2].mean(axis=0))
        centers = np.asarray(centers)
        angles = np.arctan2(centers[:, 1] - p[1], centers[:, 0] - p[0])
        return faces[np.argsort(angles)].astype(int)

    def edge_to_face(self):
        """返回每条无向 Edge 相邻的 Face。"""
        result = [[] for _ in range(self.number_of_edges)]
        for h, e in enumerate(self.edge):
            f = int(self.face[h])
            if f not in result[int(e)]:
                result[int(e)].append(f)
        return tuple(tuple(items) for items in result)

    def face_to_edge(self):
        """返回每个 Face 对应的有序全局 Edge ID。"""
        return tuple(self.edge[self.face_halfedges(f)].copy() for f in range(self.number_of_faces))
