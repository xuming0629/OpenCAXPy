#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : quadrangle.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : Quad4 一致加密
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

import numpy as np

from ..factory import create_mesh
from .common import edge_midpoint_nodes, validate_cell_type, validate_levels


def uniform_refine_quadrangle(mesh, levels: int = 1):
    """Quad4 一致加密：每个四边形 1 -> 4。"""
    validate_cell_type(mesh, "quad4")
    levels = validate_levels(levels)

    refined = mesh
    for _ in range(levels):
        points, edge_mid_ids = edge_midpoint_nodes(refined)
        c2e = refined.cell_to_edge()

        # 每个 Cell 新建一个 Cell center；它不与其他 Cell 共享。
        centers = refined.entity_barycenter("cell")
        center_start = len(points)
        center_ids = np.arange(center_start, center_start + len(centers), dtype=int)
        points = np.vstack((points, centers))

        cells = []
        for cell_id, cell in enumerate(refined.cells):
            v0, v1, v2, v3 = map(int, cell)
            m01 = int(edge_mid_ids[c2e[cell_id, 0]])
            m12 = int(edge_mid_ids[c2e[cell_id, 1]])
            m23 = int(edge_mid_ids[c2e[cell_id, 2]])
            m30 = int(edge_mid_ids[c2e[cell_id, 3]])
            c = int(center_ids[cell_id])

            cells.extend(
                (
                    (v0, m01, c, m30),
                    (m01, v1, m12, c),
                    (c, m12, v2, m23),
                    (m30, c, m23, v3),
                )
            )

        refined = create_mesh(points, np.asarray(cells, dtype=int), "quad4")

    return refined
