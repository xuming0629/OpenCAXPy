#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : tetrahedron.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : Tetra4 一致加密
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

import numpy as np

from ..factory import create_mesh
from .common import edge_midpoint_nodes, validate_cell_type, validate_levels


def uniform_refine_tetrahedron(mesh, levels: int = 1):
    """
    Tetra4 一致加密：每个四面体 1 -> 8。

    六条边加入 midpoint，先形成 4 个角部 Tetra，剩余中心 Octahedron
    再沿 m01-m23 对角线分成 4 个 Tetra。
    """
    validate_cell_type(mesh, "tetra4")
    levels = validate_levels(levels)

    refined = mesh
    for _ in range(levels):
        points, edge_mid_ids = edge_midpoint_nodes(refined)
        c2e = refined.cell_to_edge()
        cells = []

        for cell_id, cell in enumerate(refined.cells):
            v0, v1, v2, v3 = map(int, cell)

            # tetra4 local_edges:
            # 0:(0,1), 1:(1,2), 2:(2,0), 3:(0,3), 4:(1,3), 5:(2,3)
            m01 = int(edge_mid_ids[c2e[cell_id, 0]])
            m12 = int(edge_mid_ids[c2e[cell_id, 1]])
            m20 = int(edge_mid_ids[c2e[cell_id, 2]])
            m03 = int(edge_mid_ids[c2e[cell_id, 3]])
            m13 = int(edge_mid_ids[c2e[cell_id, 4]])
            m23 = int(edge_mid_ids[c2e[cell_id, 5]])

            cells.extend(
                (
                    # 4 个角部 Tetra。
                    (v0, m01, m20, m03),
                    (v1, m12, m01, m13),
                    (v2, m20, m12, m23),
                    (v3, m03, m13, m23),
                    # 中央 Octahedron 沿 m01-m23 分成 4 个 Tetra。
                    (m01, m20, m03, m23),
                    (m01, m12, m20, m23),
                    (m01, m13, m12, m23),
                    (m01, m03, m13, m23),
                )
            )

        refined = create_mesh(points, np.asarray(cells, dtype=int), "tetra4")

    return refined
