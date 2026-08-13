#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : builder.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : 从二维 Cell connectivity 构造 Half-Edge 拓扑
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

import numpy as np

from .topology import HalfEdgeTopology


def build_halfedge_from_cells(cells, *, number_of_vertices=None):
    """从 Triangle/Quad/Polygon Cell 序列构造 HalfEdgeTopology。

    Parameters
    ----------
    cells : iterable[array_like]
        每个 Cell 按边界方向给出顶点 ID。推荐所有二维单元统一采用 CCW。
    number_of_vertices : int | None
        总顶点数量。若省略，则从 connectivity 最大编号推断。
    """
    cell_list = [np.asarray(c, dtype=int).reshape(-1) for c in cells]
    if any(len(c) < 3 for c in cell_list):
        raise ValueError("half-edge faces require at least 3 vertices")

    if cell_list:
        max_vertex = max(int(c.max()) for c in cell_list if c.size)
        inferred = max_vertex + 1
    else:
        inferred = 0
    nv = inferred if number_of_vertices is None else int(number_of_vertices)
    if nv < inferred:
        raise ValueError("number_of_vertices is smaller than connectivity requires")

    origin = []
    target = []
    next_ = []
    prev = []
    face = []
    face_halfedge = np.full(len(cell_list), -1, dtype=int)
    vertex_halfedge = np.full(nv, -1, dtype=int)

    # 首先为每个 Face 独立建立有向环。
    for face_id, vertices in enumerate(cell_list):
        start = len(origin)
        n = len(vertices)
        face_halfedge[face_id] = start

        if len(np.unique(vertices)) != n:
            raise ValueError(f"face {face_id} contains duplicated vertices")

        for local_id in range(n):
            h = start + local_id
            v0 = int(vertices[local_id])
            v1 = int(vertices[(local_id + 1) % n])
            origin.append(v0)
            target.append(v1)
            next_.append(start + (local_id + 1) % n)
            prev.append(start + (local_id - 1) % n)
            face.append(face_id)
            if vertex_halfedge[v0] < 0:
                vertex_halfedge[v0] = h

    nh = len(origin)
    twin = np.full(nh, -1, dtype=int)
    edge = np.full(nh, -1, dtype=int)

    directed = {}
    undirected = {}
    edges = []

    for h, (a, b) in enumerate(zip(origin, target)):
        if a == b:
            raise ValueError(f"degenerate half-edge {h}: identical endpoints")

        reverse = (b, a)
        if reverse in directed:
            ht = directed[reverse]
            if twin[ht] >= 0:
                raise ValueError(
                    "non-manifold edge detected: more than two faces share one edge"
                )
            twin[h] = ht
            twin[ht] = h
        if (a, b) in directed:
            raise ValueError(
                "duplicate directed edge detected; face orientations may be inconsistent"
            )
        directed[(a, b)] = h

        key = (a, b) if a < b else (b, a)
        eid = undirected.get(key)
        if eid is None:
            eid = len(edges)
            undirected[key] = eid
            edges.append(key)
        edge[h] = eid

    return HalfEdgeTopology(
        origin=np.asarray(origin, dtype=int),
        target=np.asarray(target, dtype=int),
        next_=np.asarray(next_, dtype=int),
        prev=np.asarray(prev, dtype=int),
        twin=twin,
        face=np.asarray(face, dtype=int),
        edge=edge,
        face_halfedge=face_halfedge,
        vertex_halfedge=vertex_halfedge,
        edges=np.asarray(edges, dtype=int).reshape(-1, 2),
    )


def build_halfedge(mesh):
    """从 OpenCAXPy 二维 Mesh/PolygonMesh 构造 HalfEdgeTopology。"""
    if getattr(mesh, "topological_dimension", None) != 2:
        raise ValueError("Half-Edge topology currently supports 2D meshes only")

    if hasattr(mesh, "iter_cells"):
        cells = list(mesh.iter_cells())
    else:
        cells = list(mesh.cells)

    return build_halfedge_from_cells(
        cells,
        number_of_vertices=mesh.number_of_nodes(),
    )
