#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : common.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy 网格加密公共工具
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

import numpy as np


def validate_levels(levels: int) -> int:
    """检查并标准化一致加密层数。"""
    if not isinstance(levels, (int, np.integer)) or levels < 0:
        raise ValueError("levels must be a non-negative integer")
    return int(levels)


def validate_cell_type(mesh, expected: str) -> None:
    """检查 Mesh 是否为指定 CellType。"""
    if str(mesh.cell_type).lower() != expected:
        raise TypeError(
            f"refinement requires {expected!r} mesh, "
            f"got {mesh.cell_type!r}"
        )


def edge_midpoint_nodes(mesh):
    """
    为 Mesh 的每条全局 Edge 创建且只创建一个中点节点。

    Returns
    -------
    points : numpy.ndarray
        原节点 + 所有 Edge midpoint。
    midpoint_ids : numpy.ndarray
        midpoint_ids[global_edge_id] -> 新节点 ID。
    """
    edges = mesh.entity("edge")
    if len(edges) == 0:
        return mesh.points.copy(), np.empty(0, dtype=int)

    midpoint_coords = 0.5 * (
        mesh.points[edges[:, 0]] + mesh.points[edges[:, 1]]
    )
    start = mesh.number_of_nodes()
    midpoint_ids = np.arange(start, start + len(edges), dtype=int)
    points = np.vstack((mesh.points, midpoint_coords))
    return points, midpoint_ids


def append_points(points, new_points):
    """向节点数组追加节点并返回新节点编号。"""
    points = np.asarray(points, dtype=float)
    new_points = np.asarray(new_points, dtype=float)
    if new_points.size == 0:
        return points.copy(), np.empty(0, dtype=int)
    if new_points.ndim == 1:
        new_points = new_points[None, :]
    start = len(points)
    ids = np.arange(start, start + len(new_points), dtype=int)
    return np.vstack((points, new_points)), ids


def selected_cell_mask(num_cells: int, marked_cells=None) -> np.ndarray:
    """将 marked_cells 转换成布尔 Cell mask。None 表示全部 Cell。"""
    if marked_cells is None:
        return np.ones(num_cells, dtype=bool)

    marked = np.asarray(marked_cells)
    if marked.dtype == bool:
        if marked.ndim != 1 or len(marked) != num_cells:
            raise ValueError("boolean marked_cells must have shape (NC,)")
        return marked.copy()

    marked = np.asarray(marked_cells, dtype=int).reshape(-1)
    if marked.size and (marked.min() < 0 or marked.max() >= num_cells):
        raise IndexError("marked cell index out of range")

    mask = np.zeros(num_cells, dtype=bool)
    mask[marked] = True
    return mask


def coordinate_key(point, digits: int = 14):
    """为树网格节点生成稳定的几何去重 key。"""
    return tuple(np.round(np.asarray(point, dtype=float), digits).tolist())
