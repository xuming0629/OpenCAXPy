#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : quadtree.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : 二维四叉树层次网格
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ..factory import create_mesh
from .common import coordinate_key


@dataclass
class QuadtreeCell:
    """四叉树节点；仅 leaf cell 参与最终网格。"""

    bounds: tuple[float, float, float, float]
    level: int = 0
    parent: "QuadtreeCell | None" = None
    children: list["QuadtreeCell"] = field(default_factory=list)

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def refine(self):
        """当前叶节点 1 -> 4；已加密节点重复调用时保持不变。"""
        if not self.is_leaf:
            return self.children

        xmin, xmax, ymin, ymax = self.bounds
        xm = 0.5 * (xmin + xmax)
        ym = 0.5 * (ymin + ymax)
        level = self.level + 1

        self.children = [
            QuadtreeCell((xmin, xm, ymin, ym), level, self),
            QuadtreeCell((xm, xmax, ymin, ym), level, self),
            QuadtreeCell((xm, xmax, ym, ymax), level, self),
            QuadtreeCell((xmin, xm, ym, ymax), level, self),
        ]
        return self.children


class Quadtree:
    """
    二维四叉树。

    四叉树的核心不是另一种 Quad4 单元，而是保存：
        parent / children / level / leaf
    的局部自适应层次结构。

    ``to_mesh()`` 可把所有 leaf 转换成 Quad4 Mesh。若不同层级叶单元直接
    相邻，输出中可能存在 hanging node；后续 FEM 可通过 2:1 balance +
    constraint，或进一步做 conforming closure 处理。
    """

    def __init__(self, box=(0.0, 1.0, 0.0, 1.0)):
        if len(box) != 4:
            raise ValueError("box must be (xmin, xmax, ymin, ymax)")
        xmin, xmax, ymin, ymax = map(float, box)
        if xmax <= xmin or ymax <= ymin:
            raise ValueError("invalid quadtree box")
        self.root = QuadtreeCell((xmin, xmax, ymin, ymax))

    def leaves(self):
        """按深度优先顺序返回当前所有 leaf。"""
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
        """所有 leaf 一致加密指定层数。"""
        if not isinstance(levels, int) or levels < 0:
            raise ValueError("levels must be a non-negative integer")
        for _ in range(levels):
            for cell in list(self.leaves()):
                cell.refine()
        return self

    def refine(self, leaf_indices):
        """按当前 leaves() 编号局部加密。"""
        leaves = self.leaves()
        ids = np.asarray(leaf_indices, dtype=int).reshape(-1)
        if ids.size and (ids.min() < 0 or ids.max() >= len(leaves)):
            raise IndexError("quadtree leaf index out of range")
        for i in sorted(set(map(int, ids))):
            leaves[i].refine()
        return self

    @property
    def max_level(self) -> int:
        leaves = self.leaves()
        return max((cell.level for cell in leaves), default=0)

    def to_mesh(self):
        """将所有 leaf 转换成 OpenCAXPy Quad4 Mesh。"""
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
            xmin, xmax, ymin, ymax = leaf.bounds
            cells.append(
                (
                    node_id((xmin, ymin)),
                    node_id((xmax, ymin)),
                    node_id((xmax, ymax)),
                    node_id((xmin, ymax)),
                )
            )

        return create_mesh(
            np.asarray(points, dtype=float),
            np.asarray(cells, dtype=int),
            "quad4",
        )
