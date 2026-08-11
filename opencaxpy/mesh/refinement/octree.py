#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : octree.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : 三维八叉树层次网格
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ..factory import create_mesh
from .common import coordinate_key


@dataclass
class OctreeCell:
    """八叉树节点；每次 refinement 产生 8 个 children。"""

    bounds: tuple[float, float, float, float, float, float]
    level: int = 0
    parent: "OctreeCell | None" = None
    children: list["OctreeCell"] = field(default_factory=list)

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def refine(self):
        if not self.is_leaf:
            return self.children

        xmin, xmax, ymin, ymax, zmin, zmax = self.bounds
        xm = 0.5 * (xmin + xmax)
        ym = 0.5 * (ymin + ymax)
        zm = 0.5 * (zmin + zmax)
        level = self.level + 1

        self.children = []
        for k, (za, zb) in enumerate(((zmin, zm), (zm, zmax))):
            for j, (ya, yb) in enumerate(((ymin, ym), (ym, ymax))):
                for i, (xa, xb) in enumerate(((xmin, xm), (xm, xmax))):
                    self.children.append(
                        OctreeCell((xa, xb, ya, yb, za, zb), level, self)
                    )
        return self.children


class Octree:
    """
    三维八叉树层次网格。

    用于 Hexa 型空间的局部自适应 refinement。``to_mesh()`` 输出所有 leaf
    对应的 Hexa8；不同 level 邻接时可能存在 hanging node，后续可继续实现
    2:1 balance 与约束消元。
    """

    def __init__(self, box=(0.0, 1.0, 0.0, 1.0, 0.0, 1.0)):
        if len(box) != 6:
            raise ValueError(
                "box must be (xmin, xmax, ymin, ymax, zmin, zmax)"
            )
        xmin, xmax, ymin, ymax, zmin, zmax = map(float, box)
        if xmax <= xmin or ymax <= ymin or zmax <= zmin:
            raise ValueError("invalid octree box")
        self.root = OctreeCell((xmin, xmax, ymin, ymax, zmin, zmax))

    def leaves(self):
        result = []
        stack = [self.root]
        while stack:
            cell = stack.pop()
            if cell.is_leaf:
                result.append(cell)
            else:
                stack.extend(reversed(cell.children))
        return result

    def uniform_refine(self, levels: int = 1):
        if not isinstance(levels, int) or levels < 0:
            raise ValueError("levels must be a non-negative integer")
        for _ in range(levels):
            for cell in list(self.leaves()):
                cell.refine()
        return self

    def refine(self, leaf_indices):
        leaves = self.leaves()
        ids = np.asarray(leaf_indices, dtype=int).reshape(-1)
        if ids.size and (ids.min() < 0 or ids.max() >= len(leaves)):
            raise IndexError("octree leaf index out of range")
        for i in sorted(set(map(int, ids))):
            leaves[i].refine()
        return self

    @property
    def max_level(self) -> int:
        leaves = self.leaves()
        return max((cell.level for cell in leaves), default=0)

    def to_mesh(self):
        """将所有 leaf 转换成 OpenCAXPy Hexa8 Mesh。"""
        points = []
        point_ids = {}
        cells = []

        def node_id(point):
            key = coordinate_key(point)
            if key not in point_ids:
                point_ids[key] = len(points)
                points.append(tuple(map(float, point)))
            return point_ids[key]

        for leaf in self.leaves():
            xmin, xmax, ymin, ymax, zmin, zmax = leaf.bounds
            cells.append(
                (
                    node_id((xmin, ymin, zmin)),
                    node_id((xmax, ymin, zmin)),
                    node_id((xmax, ymax, zmin)),
                    node_id((xmin, ymax, zmin)),
                    node_id((xmin, ymin, zmax)),
                    node_id((xmax, ymin, zmax)),
                    node_id((xmax, ymax, zmax)),
                    node_id((xmin, ymax, zmax)),
                )
            )

        return create_mesh(
            np.asarray(points, dtype=float),
            np.asarray(cells, dtype=int),
            "hexa8",
        )
