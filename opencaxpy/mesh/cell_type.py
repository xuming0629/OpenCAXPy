#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : cell_type.py
# @Time          : 2026-08-11 09:50:55
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy 基础网格单元类型定义与查询
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CellType:
    """描述标准单元的局部拓扑信息。"""

    name: str
    dimension: int
    num_nodes: int
    local_edges: tuple[tuple[int, ...], ...] = ()
    local_faces: tuple[tuple[int, ...], ...] = ()


CELL_TYPES = {
    "line2": CellType(
        "line2", 1, 2,
        ((0, 1),),
    ),
    "triangle3": CellType(
        "triangle3", 2, 3,
        (
            (1, 2),  # edge 0: vertex 0 的对边
            (2, 0),  # edge 1: vertex 1 的对边
            (0, 1),  # edge 2: vertex 2 的对边
        ),
    ),
    "quad4": CellType(
        "quad4", 2, 4,
        ((0, 1), (1, 2), (2, 3), (3, 0)),
    ),
    "tetra4": CellType(
        "tetra4", 3, 4,
        (
            (0, 1), (1, 2), (2, 0),
            (0, 3), (1, 3), (2, 3),
        ),
        (
            (1, 2, 3),  # face 0: vertex 0 的对面
            (0, 3, 2),  # face 1: vertex 1 的对面
            (0, 1, 3),  # face 2: vertex 2 的对面
            (0, 2, 1),  # face 3: vertex 3 的对面
        ),
    ),
    "hexa8": CellType(
        "hexa8", 3, 8,
        (
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7),
        ),
        (
            (0, 3, 2, 1),
            (4, 5, 6, 7),
            (0, 1, 5, 4),
            (1, 2, 6, 5),
            (2, 3, 7, 6),
            (3, 0, 4, 7),
        ),
    ),
}


def get_cell_type(name: str) -> CellType:
    """根据名称获取 CellType，名称不区分大小写。"""
    key = str(name).lower()
    try:
        return CELL_TYPES[key]
    except KeyError as exc:
        raise KeyError(
            f"Unsupported cell type {name!r}. "
            f"Available cell types: {tuple(CELL_TYPES.keys())}"
        ) from exc
