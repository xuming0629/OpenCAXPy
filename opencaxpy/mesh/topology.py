#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : topology.py
# @Time          : 2026-08-11 09:54:01
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy 网格拓扑实体及邻接关系构建
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

import numpy as np

from .cell_type import get_cell_type


class MeshTopology:
    """根据 Cell connectivity 构造全局 Edge/Face 及邻接关系。"""

    def __init__(self, cells, cell_type):
        self.cells = np.asarray(cells, dtype=int)
        self.cell_type = str(cell_type).lower()
        self.descriptor = get_cell_type(self.cell_type)

        self.edges, self._cell_to_edge = self._build(
            self.descriptor.local_edges
        )

        if self.descriptor.dimension == 3:
            self.faces, self._cell_to_face = self._build(
                self.descriptor.local_faces
            )
        else:
            self.faces = np.empty((0, 0), dtype=int)
            self._cell_to_face = np.empty((len(self.cells), 0), dtype=int)

        self._edge_to_cell = self._reverse(self._cell_to_edge)
        self._face_to_cell = self._reverse(self._cell_to_face)

    def _build(self, local_entities):
        """由局部实体定义生成全局唯一实体和 Cell->Entity 映射。"""
        if not local_entities:
            return (
                np.empty((0, 0), dtype=int),
                np.empty((len(self.cells), 0), dtype=int),
            )

        table: dict[tuple[int, ...], int] = {}
        entities: list[tuple[int, ...]] = []
        cell_to_entity = np.empty(
            (len(self.cells), len(local_entities)), dtype=int
        )

        for cell_id, cell in enumerate(self.cells):
            for local_id, local in enumerate(local_entities):
                # 排序仅用于全局唯一化；局部方向仍由 CellType 保存。
                key = tuple(sorted(int(cell[j]) for j in local))
                entity_id = table.get(key)
                if entity_id is None:
                    entity_id = len(entities)
                    table[key] = entity_id
                    entities.append(key)
                cell_to_entity[cell_id, local_id] = entity_id

        return np.asarray(entities, dtype=int), cell_to_entity

    @staticmethod
    def _reverse(cell_to_entity):
        """由 Cell->Entity 生成 Entity->Cell 邻接关系。"""
        if not cell_to_entity.size:
            return tuple()

        result = [[] for _ in range(int(cell_to_entity.max()) + 1)]
        for cell_id, row in enumerate(cell_to_entity):
            for entity_id in row:
                result[int(entity_id)].append(cell_id)
        return tuple(tuple(items) for items in result)

    def cell_to_edge(self):
        return self._cell_to_edge.copy()

    def cell_to_face(self):
        return self._cell_to_face.copy()

    def edge_to_cell(self):
        return self._edge_to_cell

    def face_to_cell(self):
        return self._face_to_cell

    def boundary_node_index(self):
        """返回边界 Node 全局编号。"""
        if self.cells.size == 0:
            return np.empty(0, dtype=int)

        if self.descriptor.dimension == 1:
            nodes, counts = np.unique(
                self.cells.reshape(-1), return_counts=True
            )
            return nodes[counts == 1].astype(int)

        if self.descriptor.dimension == 2:
            edge_ids = self.boundary_edge_index()
            if edge_ids.size == 0:
                return np.empty(0, dtype=int)
            return np.unique(self.edges[edge_ids].reshape(-1)).astype(int)

        face_ids = self.boundary_face_index()
        if face_ids.size == 0:
            return np.empty(0, dtype=int)
        return np.unique(self.faces[face_ids].reshape(-1)).astype(int)

    def boundary_edge_index(self):
        """返回边界 Edge 全局编号。"""
        if self.descriptor.dimension == 1:
            return np.arange(len(self.edges), dtype=int)

        if self.descriptor.dimension == 2:
            return np.asarray(
                [i for i, adj in enumerate(self._edge_to_cell) if len(adj) == 1],
                dtype=int,
            )

        boundary_faces = self.faces[self.boundary_face_index()]
        if boundary_faces.size == 0:
            return np.empty(0, dtype=int)

        boundary_sets = [set(map(int, face)) for face in boundary_faces]
        ids = []
        for edge_id, edge in enumerate(self.edges):
            nodes = set(map(int, edge))
            if any(nodes.issubset(face) for face in boundary_sets):
                ids.append(edge_id)
        return np.asarray(ids, dtype=int)

    def boundary_face_index(self):
        """返回三维体网格的边界 Face 全局编号。"""
        if self.descriptor.dimension != 3:
            return np.empty(0, dtype=int)
        return np.asarray(
            [i for i, adj in enumerate(self._face_to_cell) if len(adj) == 1],
            dtype=int,
        )
