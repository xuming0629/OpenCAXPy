#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : hexahedron.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : Hexa8 一致加密
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

import numpy as np

from ..factory import create_mesh
from .common import edge_midpoint_nodes, validate_cell_type, validate_levels


def uniform_refine_hexahedron(mesh, levels: int = 1):
    """
    Hexa8 一致加密：每个六面体 1 -> 8。

    新节点由三类实体产生：
        - 12 个 Edge midpoint（全局 Edge 共享）；
        - 6 个 Face center（全局 Face 共享）；
        - 1 个 Cell center（Cell 独占）。
    """
    validate_cell_type(mesh, "hexa8")
    levels = validate_levels(levels)

    refined = mesh
    for _ in range(levels):
        # ------------------------------------------------------------
        # Edge midpoint
        # ------------------------------------------------------------
        points, edge_mid_ids = edge_midpoint_nodes(refined)
        c2e = refined.cell_to_edge()
        c2f = refined.cell_to_face()

        # ------------------------------------------------------------
        # Face center：每个全局 Face 只创建一次。
        # ------------------------------------------------------------
        faces = refined.entity("face")
        face_centers = refined.points[faces].mean(axis=1)
        face_start = len(points)
        face_center_ids = np.arange(
            face_start, face_start + len(face_centers), dtype=int
        )
        points = np.vstack((points, face_centers))

        # ------------------------------------------------------------
        # Cell center
        # ------------------------------------------------------------
        cell_centers = refined.entity_barycenter("cell")
        cell_start = len(points)
        cell_center_ids = np.arange(
            cell_start, cell_start + len(cell_centers), dtype=int
        )
        points = np.vstack((points, cell_centers))

        cells = []

        for cell_id, cell in enumerate(refined.cells):
            v = list(map(int, cell))

            # 构造当前父 Hexa 的 3 x 3 x 3 局部节点格点。
            n: dict[tuple[int, int, int], int] = {}

            # 8 vertices。
            n[(0, 0, 0)] = v[0]
            n[(2, 0, 0)] = v[1]
            n[(2, 2, 0)] = v[2]
            n[(0, 2, 0)] = v[3]
            n[(0, 0, 2)] = v[4]
            n[(2, 0, 2)] = v[5]
            n[(2, 2, 2)] = v[6]
            n[(0, 2, 2)] = v[7]

            # 12 edge midpoints，顺序与 hexa8 local_edges 一致。
            edge_lattice = (
                (1, 0, 0), (2, 1, 0), (1, 2, 0), (0, 1, 0),
                (1, 0, 2), (2, 1, 2), (1, 2, 2), (0, 1, 2),
                (0, 0, 1), (2, 0, 1), (2, 2, 1), (0, 2, 1),
            )
            for local_edge_id, lattice in enumerate(edge_lattice):
                n[lattice] = int(edge_mid_ids[c2e[cell_id, local_edge_id]])

            # 6 face centers，顺序与 hexa8 local_faces 一致。
            face_lattice = (
                (1, 1, 0),  # bottom
                (1, 1, 2),  # top
                (1, 0, 1),  # front
                (2, 1, 1),  # right
                (1, 2, 1),  # back
                (0, 1, 1),  # left
            )
            for local_face_id, lattice in enumerate(face_lattice):
                n[lattice] = int(face_center_ids[c2f[cell_id, local_face_id]])

            # Cell center。
            n[(1, 1, 1)] = int(cell_center_ids[cell_id])

            # 2 x 2 x 2 = 8 个 child Hexa8。
            for k in range(2):
                for j in range(2):
                    for i in range(2):
                        x0, x1 = i, i + 1
                        y0, y1 = j, j + 1
                        z0, z1 = k, k + 1
                        cells.append(
                            (
                                n[(x0, y0, z0)],
                                n[(x1, y0, z0)],
                                n[(x1, y1, z0)],
                                n[(x0, y1, z0)],
                                n[(x0, y0, z1)],
                                n[(x1, y0, z1)],
                                n[(x1, y1, z1)],
                                n[(x0, y1, z1)],
                            )
                        )

        refined = create_mesh(points, np.asarray(cells, dtype=int), "hexa8")

    return refined
