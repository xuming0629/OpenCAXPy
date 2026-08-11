#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : triangle.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : Triangle3 二分加密与一致加密
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

import numpy as np

from ..factory import create_mesh
from .common import (
    edge_midpoint_nodes,
    selected_cell_mask,
    validate_cell_type,
    validate_levels,
)


def uniform_refine_triangle(mesh, levels: int = 1):
    """
    Triangle3 红色一致加密（red refinement）：每个三角形 1 -> 4。

    所有全局 Edge midpoint 只创建一次，因此相邻单元天然共享中点节点，
    加密后的网格保持 conforming。
    """
    validate_cell_type(mesh, "triangle3")
    levels = validate_levels(levels)

    refined = mesh
    for _ in range(levels):
        points, edge_mid_ids = edge_midpoint_nodes(refined)
        c2e = refined.cell_to_edge()
        cells = []

        for cell_id, cell in enumerate(refined.cells):
            v0, v1, v2 = map(int, cell)

            # Triangle3 local_edges:
            #   edge 0 = (1, 2) -> m12
            #   edge 1 = (2, 0) -> m20
            #   edge 2 = (0, 1) -> m01
            m12 = int(edge_mid_ids[c2e[cell_id, 0]])
            m20 = int(edge_mid_ids[c2e[cell_id, 1]])
            m01 = int(edge_mid_ids[c2e[cell_id, 2]])

            cells.extend(
                (
                    (v0, m01, m20),
                    (m01, v1, m12),
                    (m20, m12, v2),
                    (m01, m12, m20),
                )
            )

        refined = create_mesh(points, np.asarray(cells, dtype=int), "triangle3")

    return refined


def _triangle_edge_lengths(mesh):
    """返回每个 Cell 三条局部边的长度。"""
    return mesh.edge_length()[mesh.cell_to_edge()]


def bisect_triangle(mesh, marked_cells=None):
    """
    Triangle3 局部二分加密。

    对每个 marked Cell 选择最长边作为二分边。所有被选中的全局边统一创建
    midpoint。为保证共享边两侧没有 hanging node，相邻单元根据其被切分边数量
    自动采用 1-edge / 2-edge / 3-edge 闭合模板：

        0 条切分边 -> 1 个 Triangle
        1 条切分边 -> 2 个 Triangle
        2 条切分边 -> 3 个 Triangle
        3 条切分边 -> 4 个 Triangle

    这是一套轻量级 conforming red-green refinement，适合作为 OpenCAXPy
    第一版 Triangle 局部加密基础。
    """
    validate_cell_type(mesh, "triangle3")
    marked_mask = selected_cell_mask(mesh.number_of_cells(), marked_cells)

    c2e = mesh.cell_to_edge()
    edge_lengths = _triangle_edge_lengths(mesh)

    # 每个 marked Cell 选择最长局部边；共享的是全局 edge id。
    split_edge_ids: set[int] = set()
    for cell_id in np.flatnonzero(marked_mask):
        local_edge = int(np.argmax(edge_lengths[cell_id]))
        split_edge_ids.add(int(c2e[cell_id, local_edge]))

    if not split_edge_ids:
        return create_mesh(mesh.points.copy(), mesh.cells.copy(), "triangle3")

    # 只为真正需要切分的全局 Edge 创建 midpoint。
    points_list = [p.copy() for p in mesh.points]
    midpoint: dict[int, int] = {}
    edges = mesh.entity("edge")
    for edge_id in sorted(split_edge_ids):
        a, b = map(int, edges[edge_id])
        midpoint[edge_id] = len(points_list)
        points_list.append(0.5 * (mesh.points[a] + mesh.points[b]))

    new_cells: list[tuple[int, int, int]] = []

    for cell_id, cell in enumerate(mesh.cells):
        v0, v1, v2 = map(int, cell)
        e0, e1, e2 = map(int, c2e[cell_id])
        s0 = e0 in split_edge_ids  # v1-v2
        s1 = e1 in split_edge_ids  # v2-v0
        s2 = e2 in split_edge_ids  # v0-v1
        nsplit = int(s0) + int(s1) + int(s2)

        if nsplit == 0:
            new_cells.append((v0, v1, v2))
            continue

        m0 = midpoint.get(e0)  # m12
        m1 = midpoint.get(e1)  # m20
        m2 = midpoint.get(e2)  # m01

        if nsplit == 1:
            if s0:
                new_cells.extend(((v0, v1, m0), (v0, m0, v2)))
            elif s1:
                new_cells.extend(((v1, v2, m1), (v1, m1, v0)))
            else:  # s2
                new_cells.extend(((v2, v0, m2), (v2, m2, v1)))
            continue

        if nsplit == 2:
            if s0 and s1:
                # 两条切分边在 v2 相交。
                new_cells.extend(
                    ((v2, m1, m0), (v0, v1, m0), (v0, m0, m1))
                )
            elif s1 and s2:
                # 两条切分边在 v0 相交。
                new_cells.extend(
                    ((v0, m2, m1), (v1, v2, m1), (v1, m1, m2))
                )
            else:  # s2 and s0，在 v1 相交。
                new_cells.extend(
                    ((v1, m0, m2), (v2, v0, m2), (v2, m2, m0))
                )
            continue

        # 三条 Edge 都被切分：标准 1 -> 4 red refinement。
        new_cells.extend(
            (
                (v0, m2, m1),
                (m2, v1, m0),
                (m1, m0, v2),
                (m2, m0, m1),
            )
        )

    return create_mesh(
        np.asarray(points_list, dtype=float),
        np.asarray(new_cells, dtype=int),
        "triangle3",
    )
