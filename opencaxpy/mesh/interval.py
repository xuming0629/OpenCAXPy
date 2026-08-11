#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : interval.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy Line2 一维区间网格
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

import numpy as np

from .mesh import Mesh


class IntervalMesh(Mesh):
    """
    二节点线单元区间网格。

    IntervalMesh 是基于 ``line2`` 单元类型的一维网格实现。

    每个 Line2 Cell 包含两个局部节点：

        local vertex 0:
            起点

        local vertex 1:
            终点

    对规则区间网格：

        0 ---- 1 ---- 2 ---- 3 ---- 4

    对应单元连接关系：

        cell 0:
            (0, 1)

        cell 1:
            (1, 2)

        cell 2:
            (2, 3)

        cell 3:
            (3, 4)

    Parameters
    ----------
    points : array_like
        网格节点坐标。

        可以输入一维数组：

            shape = (NN,)

        例如：

            [0.0, 0.5, 1.0]

        也可以输入 OpenCAXPy 标准二维数组：

            shape = (NN, 1)

        例如：

            [
                [0.0],
                [0.5],
                [1.0],
            ]

    cells : array_like
        Line2 单元连接关系。

        shape:

            (NC, 2)
    """

    def __init__(
        self,
        points,
        cells,
    ):
        """
        初始化 Line2 区间网格。

        Parameters
        ----------
        points : array_like
            节点坐标。

        cells : array_like
            Line2 单元连接关系。
        """

        # ------------------------------------------------------------
        # 标准化节点坐标
        # ------------------------------------------------------------

        points = np.asarray(
            points,
            dtype=float,
        )

        # 用户可能直接输入：
        #
        #     [0.0, 0.5, 1.0]
        #
        # 此时 shape 为：
        #
        #     (NN,)
        #
        # OpenCAXPy Mesh 统一要求：
        #
        #     (NN, GD)
        #
        # 因此一维网格转换成：
        #
        #     (NN, 1)
        #
        if points.ndim == 1:
            points = points[:, None]

        # ------------------------------------------------------------
        # 初始化通用 Mesh
        # ------------------------------------------------------------

        super().__init__(
            points,
            cells,
            "line2",
        )

    @classmethod
    def from_interval(
        cls,
        interval=(0.0, 1.0),
        n=1,
    ):
        """
        在指定一维区间上生成规则 Line2 网格。

        该方法是 ``generate_interval`` 的便捷封装。

        实际网格生成算法位于：

            opencaxpy.mesh.generators.interval

        Parameters
        ----------
        interval : tuple[float, float]
            一维区间：

                (xmin, xmax)

        n : int
            区间划分数量。

            最终生成：

                n 个 Line2 Cell
                n + 1 个 Node

        Returns
        -------
        IntervalMesh
            生成的一维规则区间网格。

        Examples
        --------
        >>> mesh = IntervalMesh.from_interval(
        ...     interval=(0.0, 10.0),
        ...     n=10,
        ... )
        >>>
        >>> mesh.number_of_nodes()
        11
        >>>
        >>> mesh.number_of_cells()
        10
        """

        # ------------------------------------------------------------
        # 延迟导入 Generator
        # ------------------------------------------------------------
        #
        # IntervalMesh 只负责表示一维网格，
        # 实际规则网格生成算法放在 generators/ 中。
        #
        from .generators.interval import generate_interval

        # ------------------------------------------------------------
        # 生成 points + cells
        # ------------------------------------------------------------

        points, cells = generate_interval(
            interval=interval,
            n=n,
        )

        # ------------------------------------------------------------
        # 创建 IntervalMesh
        # ------------------------------------------------------------

        return cls(
            points,
            cells,
        )
