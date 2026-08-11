#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : interval.py
# @Time          : 2026-08-11 10:32:24
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy 一维规则区间 Line2 网格生成器
# @Company       : 2026 XuMing. All Rights Reserved.
"""

import numpy as np


def generate_interval(
    interval=(0.0, 1.0),
    n=1,
):
    """
    在一维区间上生成规则 Line2 网格。

    Parameters
    ----------
    interval : tuple[float, float]
        一维区间范围：

            (xmin, xmax)

    n : int
        区间划分数量。

        最终生成：

            n 个 Line2 单元
            n + 1 个节点

    Returns
    -------
    points : numpy.ndarray
        节点坐标。

        shape:

            (n + 1, 1)

    cells : numpy.ndarray
        Line2 单元连接关系。

        shape:

            (n, 2)

    Notes
    -----
    节点按照从 xmin 到 xmax 的方向依次编号。

    例如：

        interval = (0.0, 1.0)
        n = 4

    节点编号：

        0 ---- 1 ---- 2 ---- 3 ---- 4

    单元连接关系：

        cell 0:
            (0, 1)

        cell 1:
            (1, 2)

        cell 2:
            (2, 3)

        cell 3:
            (3, 4)

    因此所有 Line2 单元均具有一致的正向局部编号：

        local vertex 0 -> 左端点
        local vertex 1 -> 右端点
    """

    # ------------------------------------------------------------
    # 检查 interval 参数
    # ------------------------------------------------------------

    if len(interval) != 2:
        raise ValueError("interval must be (xmin, xmax)")

    xmin, xmax = map(
        float,
        interval,
    )

    # 区间长度必须为正。
    if xmax <= xmin:
        raise ValueError("xmax must be greater than xmin")

    # ------------------------------------------------------------
    # 检查划分数量
    # ------------------------------------------------------------

    if (
        not isinstance(
            n,
            (int, np.integer),
        )
        or n <= 0
    ):
        raise ValueError("n must be a positive integer")

    # ------------------------------------------------------------
    # 生成节点
    # ------------------------------------------------------------

    # 生成：
    #
    #     n + 1
    #
    # 个等间距节点。
    #
    # 使用 [:, None] 将：
    #
    #     (n + 1,)
    #
    # 转换成 OpenCAXPy Mesh 统一要求的：
    #
    #     (n + 1, 1)
    #
    points = np.linspace(
        xmin,
        xmax,
        n + 1,
        dtype=float,
    )[:, None]

    # ------------------------------------------------------------
    # 构造 Line2 单元
    # ------------------------------------------------------------

    # 左端节点：
    #
    #     0, 1, 2, ..., n-1
    #
    left = np.arange(
        n,
        dtype=int,
    )

    # 右端节点：
    #
    #     1, 2, 3, ..., n
    #
    right = np.arange(
        1,
        n + 1,
        dtype=int,
    )

    # 合并成：
    #
    #     [
    #         [0, 1],
    #         [1, 2],
    #         [2, 3],
    #         ...
    #     ]
    #
    cells = np.column_stack(
        (
            left,
            right,
        )
    )

    return (
        points,
        cells,
    )
