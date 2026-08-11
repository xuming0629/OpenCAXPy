#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : box3d.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy 三维长方体区域规则 Tetra4 / Hexa8 网格生成器
# @Company       : 2026 XuMing. All Rights Reserved.
"""

import numpy as np


def _grid_points(
    box,
    nx,
    ny,
    nz,
):
    """
    生成三维长方体区域规则网格节点。

    Parameters
    ----------
    box : tuple[float, float, float, float, float, float]
        三维长方体区域范围：

            (
                xmin,
                xmax,
                ymin,
                ymax,
                zmin,
                zmax,
            )

    nx : int
        x 方向网格划分数量。

    ny : int
        y 方向网格划分数量。

    nz : int
        z 方向网格划分数量。

    Returns
    -------
    numpy.ndarray
        三维规则网格节点坐标。

        shape:

            (
                (nx + 1)
                * (ny + 1)
                * (nz + 1),
                3,
            )

    Notes
    -----
    节点编号顺序：

        1. x 方向优先递增；
        2. 然后 y 方向逐行递增；
        3. 最后沿 z 方向逐层递增。

    即逻辑坐标：

        (i, j, k)

    对应全局节点编号：

        node_id =
            k * (ny + 1) * (nx + 1)
            + j * (nx + 1)
            + i
    """

    # ------------------------------------------------------------
    # 检查 box 参数
    # ------------------------------------------------------------

    if len(box) != 6:
        raise ValueError("box must be " "(xmin, xmax, ymin, ymax, zmin, zmax)")

    xmin, xmax, ymin, ymax, zmin, zmax = map(
        float,
        box,
    )

    # 长方体三个方向长度必须均为正。
    if xmax <= xmin or ymax <= ymin or zmax <= zmin:
        raise ValueError("box upper bounds must be greater " "than lower bounds")

    # ------------------------------------------------------------
    # 检查网格划分数量
    # ------------------------------------------------------------

    for name, value in (
        ("nx", nx),
        ("ny", ny),
        ("nz", nz),
    ):
        if (
            not isinstance(
                value,
                (int, np.integer),
            )
            or value <= 0
        ):
            raise ValueError(f"{name} must be a positive integer")

    # ------------------------------------------------------------
    # 生成三个方向的规则坐标
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

    zs = np.linspace(
        zmin,
        zmax,
        nz + 1,
    )

    # ------------------------------------------------------------
    # 构造节点坐标
    # ------------------------------------------------------------

    # 遍历顺序：
    #
    #     z
    #       ↓
    #     y
    #       ↓
    #     x
    #
    # 即 x 方向变化最快。
    #
    points = np.array(
        [(x, y, z) for z in zs for y in ys for x in xs],
        dtype=float,
    )

    return points


def _nid(
    i,
    j,
    k,
    nx,
    ny,
):
    """
    根据规则网格逻辑坐标获取全局节点编号。

    Parameters
    ----------
    i : int
        x 方向逻辑节点编号。

    j : int
        y 方向逻辑节点编号。

    k : int
        z 方向逻辑节点编号。

    nx : int
        x 方向网格划分数量。

    ny : int
        y 方向网格划分数量。

    Returns
    -------
    int
        全局节点编号。

    Notes
    -----
    每一个 z 层包含：

        (nx + 1) * (ny + 1)

    个节点。

    每一个 y 行包含：

        nx + 1

    个节点。
    """
    return k * (ny + 1) * (nx + 1) + j * (nx + 1) + i


def generate_hexa_box(
    box=(0.0, 1.0, 0.0, 1.0, 0.0, 1.0),
    nx=1,
    ny=1,
    nz=1,
):
    """
    在三维长方体区域生成规则 Hexa8 网格。

    Parameters
    ----------
    box : tuple[float, float, float, float, float, float]
        长方体区域：

            (
                xmin,
                xmax,
                ymin,
                ymax,
                zmin,
                zmax,
            )

    nx : int
        x 方向划分数量。

    ny : int
        y 方向划分数量。

    nz : int
        z 方向划分数量。

    Returns
    -------
    points : numpy.ndarray
        节点坐标。

    cells : numpy.ndarray
        Hexa8 单元连接关系。

        shape:

            (nx * ny * nz, 8)

    Notes
    -----
    Hexa8 局部节点编号采用：

               7 -------- 6
              /|         /|
             / |        / |
            4 -------- 5  |
            |  |       |  |
            |  3 ------|--2
            | /        | /
            |/         |/
            0 -------- 1

    即：

        bottom:
            0, 1, 2, 3

        top:
            4, 5, 6, 7

    该编号顺序与 OpenCAXPy 当前 Hexa8 CellType 保持一致。
    """

    # ------------------------------------------------------------
    # 生成规则三维节点
    # ------------------------------------------------------------

    points = _grid_points(
        box,
        nx,
        ny,
        nz,
    )

    cells = []

    # ------------------------------------------------------------
    # 遍历每一个规则 Hexa block
    # ------------------------------------------------------------

    for k in range(nz):
        for j in range(ny):
            for i in range(nx):

                # ------------------------------------------------
                # 当前 Hexa8 八个节点
                # ------------------------------------------------
                #
                #            n7 -------- n6
                #           /|          /|
                #          / |         / |
                #        n4 -------- n5  |
                #         |  |        |  |
                #         | n3 -------|- n2
                #         | /         | /
                #         |/          |/
                #        n0 -------- n1
                #
                n0 = _nid(
                    i,
                    j,
                    k,
                    nx,
                    ny,
                )

                n1 = _nid(
                    i + 1,
                    j,
                    k,
                    nx,
                    ny,
                )

                n2 = _nid(
                    i + 1,
                    j + 1,
                    k,
                    nx,
                    ny,
                )

                n3 = _nid(
                    i,
                    j + 1,
                    k,
                    nx,
                    ny,
                )

                n4 = _nid(
                    i,
                    j,
                    k + 1,
                    nx,
                    ny,
                )

                n5 = _nid(
                    i + 1,
                    j,
                    k + 1,
                    nx,
                    ny,
                )

                n6 = _nid(
                    i + 1,
                    j + 1,
                    k + 1,
                    nx,
                    ny,
                )

                n7 = _nid(
                    i,
                    j + 1,
                    k + 1,
                    nx,
                    ny,
                )

                cells.append(
                    (
                        n0,
                        n1,
                        n2,
                        n3,
                        n4,
                        n5,
                        n6,
                        n7,
                    )
                )

    return (
        points,
        np.asarray(
            cells,
            dtype=int,
        ),
    )


def generate_tetra_box(
    box=(0.0, 1.0, 0.0, 1.0, 0.0, 1.0),
    nx=1,
    ny=1,
    nz=1,
):
    """
    在三维长方体区域生成规则 Tetra4 网格。

    每个规则 Hexa8 网格块沿：

        n0 -> n6

    主对角线分解为 6 个 Tetra4 单元。

    Parameters
    ----------
    box : tuple[float, float, float, float, float, float]
        长方体区域：

            (
                xmin,
                xmax,
                ymin,
                ymax,
                zmin,
                zmax,
            )

    nx : int
        x 方向划分数量。

    ny : int
        y 方向划分数量。

    nz : int
        z 方向划分数量。

    Returns
    -------
    points : numpy.ndarray
        节点坐标。

    cells : numpy.ndarray
        Tetra4 单元连接关系。

        shape:

            (6 * nx * ny * nz, 4)

    Notes
    -----
    首先构造规则 Hexa8：

               n7 -------- n6
              /|          /|
             / |         / |
           n4 -------- n5  |
            |  |        |  |
            | n3 -------|- n2
            | /         | /
            |/          |/
           n0 -------- n1

    然后沿主对角线：

        n0 -> n6

    分解为 6 个四面体：

        0:
            (n0, n1, n2, n6)

        1:
            (n0, n2, n3, n6)

        2:
            (n0, n3, n7, n6)

        3:
            (n0, n7, n4, n6)

        4:
            (n0, n4, n5, n6)

        5:
            (n0, n5, n1, n6)

    相邻规则 Hexa block 使用相同的分解模式，
    因此共享面的三角剖分保持一致。
    """

    # ------------------------------------------------------------
    # 生成规则节点
    # ------------------------------------------------------------

    points = _grid_points(
        box,
        nx,
        ny,
        nz,
    )

    cells = []

    # ------------------------------------------------------------
    # 遍历每一个规则 Hexa block
    # ------------------------------------------------------------

    for k in range(nz):
        for j in range(ny):
            for i in range(nx):

                # ------------------------------------------------
                # 当前 Hexa8 的八个节点
                # ------------------------------------------------

                n0 = _nid(
                    i,
                    j,
                    k,
                    nx,
                    ny,
                )

                n1 = _nid(
                    i + 1,
                    j,
                    k,
                    nx,
                    ny,
                )

                n2 = _nid(
                    i + 1,
                    j + 1,
                    k,
                    nx,
                    ny,
                )

                n3 = _nid(
                    i,
                    j + 1,
                    k,
                    nx,
                    ny,
                )

                n4 = _nid(
                    i,
                    j,
                    k + 1,
                    nx,
                    ny,
                )

                n5 = _nid(
                    i + 1,
                    j,
                    k + 1,
                    nx,
                    ny,
                )

                n6 = _nid(
                    i + 1,
                    j + 1,
                    k + 1,
                    nx,
                    ny,
                )

                n7 = _nid(
                    i,
                    j + 1,
                    k + 1,
                    nx,
                    ny,
                )

                # ------------------------------------------------
                # Hexa8 -> 6 × Tetra4
                # ------------------------------------------------
                #
                # 六个四面体共享主对角线：
                #
                #     n0 -> n6
                #
                cells.extend(
                    (
                        (
                            n0,
                            n1,
                            n2,
                            n6,
                        ),
                        (
                            n0,
                            n2,
                            n3,
                            n6,
                        ),
                        (
                            n0,
                            n3,
                            n7,
                            n6,
                        ),
                        (
                            n0,
                            n7,
                            n4,
                            n6,
                        ),
                        (
                            n0,
                            n4,
                            n5,
                            n6,
                        ),
                        (
                            n0,
                            n5,
                            n1,
                            n6,
                        ),
                    )
                )

    return (
        points,
        np.asarray(
            cells,
            dtype=int,
        ),
    )
