#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : box2d.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy 二维矩形区域规则 Triangle3 / Quad4 网格生成器
# @Company       : 2026 XuMing. All Rights Reserved.
"""

import numpy as np


def _grid_points(
    box,
    nx,
    ny,
):
    """
    生成二维矩形区域的规则网格节点。

    该函数只负责生成规则结构化节点，不负责构造具体单元。

    Parameters
    ----------
    box : tuple[float, float, float, float]
        二维矩形区域范围：

            (xmin, xmax, ymin, ymax)

    nx : int
        x 方向网格划分数量。

        节点数量为：

            nx + 1

    ny : int
        y 方向网格划分数量。

        节点数量为：

            ny + 1

    Returns
    -------
    numpy.ndarray
        规则网格节点坐标。

        shape:

            ((nx + 1) * (ny + 1), 2)

    Notes
    -----
    节点编号顺序为：

        - x 方向优先递增；
        - y 方向逐行递增。

    例如：

        nx = 2
        ny = 2

    节点编号为：

        6 -------- 7 -------- 8
        |          |          |
        |          |          |
        3 -------- 4 -------- 5
        |          |          |
        |          |          |
        0 -------- 1 -------- 2
    """

    # ------------------------------------------------------------
    # 检查 box 参数
    # ------------------------------------------------------------

    if len(box) != 4:
        raise ValueError("box must be (xmin, xmax, ymin, ymax)")

    xmin, xmax, ymin, ymax = map(
        float,
        box,
    )

    # 矩形区域必须具有正长度和正宽度。
    if xmax <= xmin or ymax <= ymin:
        raise ValueError("box upper bounds must be greater than lower bounds")

    # ------------------------------------------------------------
    # 检查 nx
    # ------------------------------------------------------------

    if not isinstance(nx, (int, np.integer)) or nx <= 0:
        raise ValueError("nx must be a positive integer")

    # ------------------------------------------------------------
    # 检查 ny
    # ------------------------------------------------------------

    if not isinstance(ny, (int, np.integer)) or ny <= 0:
        raise ValueError("ny must be a positive integer")

    # ------------------------------------------------------------
    # 生成 x / y 方向等距坐标
    # ------------------------------------------------------------

    xs = np.linspace(
        xmin,
        xmax,
        nx + 1,
    )

    ys = np.linspace(
        ymin,
        ymax,
        ny + 1,
    )

    # ------------------------------------------------------------
    # 构造节点坐标
    # ------------------------------------------------------------

    # 节点顺序：
    #
    #     先遍历 y，
    #     每一行内部再遍历 x。
    #
    # 因此节点编号为：
    #
    #     node_id(i, j) = j * (nx + 1) + i
    #
    points = np.array(
        [(x, y) for y in ys for x in xs],
        dtype=float,
    )

    return points


def generate_triangle_box(
    box=(0.0, 1.0, 0.0, 1.0),
    nx=1,
    ny=1,
):
    """
    在二维矩形区域生成规则 Triangle3 网格。

    首先将矩形区域划分为：

        nx * ny

    个规则四边形网格块，然后将每个四边形沿：

        左下角 -> 右上角

    的对角线划分为两个 Triangle3 单元。

    Parameters
    ----------
    box : tuple[float, float, float, float]
        矩形区域：

            (xmin, xmax, ymin, ymax)

    nx : int
        x 方向网格划分数量。

    ny : int
        y 方向网格划分数量。

    Returns
    -------
    points : numpy.ndarray
        节点坐标。

        shape:

            ((nx + 1) * (ny + 1), 2)

    cells : numpy.ndarray
        Triangle3 单元连接关系。

        shape:

            (2 * nx * ny, 3)

    Notes
    -----
    每个矩形网格块的局部节点布局：

        n3 -------- n2
        |         / |
        |       /   |
        |     /     |
        |   /       |
        | /         |
        n0 -------- n1

    被划分成两个 Triangle3：

        triangle 0:
            (n0, n1, n2)

        triangle 1:
            (n0, n2, n3)

    两个三角形均保持逆时针节点方向。
    """

    # ------------------------------------------------------------
    # 生成规则节点
    # ------------------------------------------------------------

    points = _grid_points(
        box,
        nx,
        ny,
    )

    # ------------------------------------------------------------
    # 规则网格逻辑坐标 -> 全局节点编号
    # ------------------------------------------------------------

    def nid(i, j):
        """
        根据二维规则网格逻辑坐标 (i, j)
        获取对应的全局节点编号。
        """
        return j * (nx + 1) + i

    # ------------------------------------------------------------
    # 构造 Triangle3 单元
    # ------------------------------------------------------------

    cells = []

    for j in range(ny):
        for i in range(nx):

            # 当前矩形网格块：
            #
            #     n3 -------- n2
            #     |           |
            #     |           |
            #     |           |
            #     n0 -------- n1
            #
            n0 = nid(
                i,
                j,
            )

            n1 = nid(
                i + 1,
                j,
            )

            n2 = nid(
                i + 1,
                j + 1,
            )

            n3 = nid(
                i,
                j + 1,
            )

            # ----------------------------------------------------
            # Triangle 0
            # ----------------------------------------------------
            #
            # 节点顺序：
            #
            #     n0 -> n1 -> n2
            #
            # 保持逆时针方向。
            #
            cells.append(
                (
                    n0,
                    n1,
                    n2,
                )
            )

            # ----------------------------------------------------
            # Triangle 1
            # ----------------------------------------------------
            #
            # 节点顺序：
            #
            #     n0 -> n2 -> n3
            #
            # 同样保持逆时针方向。
            #
            cells.append(
                (
                    n0,
                    n2,
                    n3,
                )
            )

    return (
        points,
        np.asarray(
            cells,
            dtype=int,
        ),
    )


def generate_quad_box(
    box=(0.0, 1.0, 0.0, 1.0),
    nx=1,
    ny=1,
):
    """
    在二维矩形区域生成规则 Quad4 网格。

    Parameters
    ----------
    box : tuple[float, float, float, float]
        矩形区域：

            (xmin, xmax, ymin, ymax)

    nx : int
        x 方向网格划分数量。

    ny : int
        y 方向网格划分数量。

    Returns
    -------
    points : numpy.ndarray
        节点坐标。

        shape:

            ((nx + 1) * (ny + 1), 2)

    cells : numpy.ndarray
        Quad4 单元连接关系。

        shape:

            (nx * ny, 4)

    Notes
    -----
    每个 Quad4 的局部节点编号：

        3 -------- 2
        |          |
        |          |
        |          |
        0 -------- 1

    单元节点按照逆时针方向排列：

        (0, 1, 2, 3)
    """

    # ------------------------------------------------------------
    # 生成规则节点
    # ------------------------------------------------------------

    points = _grid_points(
        box,
        nx,
        ny,
    )

    # ------------------------------------------------------------
    # 规则网格逻辑坐标 -> 全局节点编号
    # ------------------------------------------------------------

    def nid(i, j):
        """
        根据二维规则网格逻辑坐标 (i, j)
        获取对应的全局节点编号。
        """
        return j * (nx + 1) + i

    # ------------------------------------------------------------
    # 构造 Quad4 单元
    # ------------------------------------------------------------

    cells = []

    for j in range(ny):
        for i in range(nx):

            # 当前 Quad4：
            #
            #     n3 -------- n2
            #     |           |
            #     |           |
            #     |           |
            #     n0 -------- n1
            #
            n0 = nid(
                i,
                j,
            )

            n1 = nid(
                i + 1,
                j,
            )

            n2 = nid(
                i + 1,
                j + 1,
            )

            n3 = nid(
                i,
                j + 1,
            )

            # Quad4 节点按照逆时针方向排列。
            cells.append(
                (
                    n0,
                    n1,
                    n2,
                    n3,
                )
            )

    return (
        points,
        np.asarray(
            cells,
            dtype=int,
        ),
    )
