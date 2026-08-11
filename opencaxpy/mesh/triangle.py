#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : triangle.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy Triangle3 三角形网格
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

from .mesh import Mesh


class TriangleMesh(Mesh):
    """
    三节点三角形网格。

    TriangleMesh 是基于 ``triangle3`` 单元类型的
    二维三角形网格实现。

    每个 Triangle3 Cell 包含 3 个局部节点。

    OpenCAXPy 当前采用的局部节点编号约定为：

            2
            |\
            | \
            |  \
            |   \
            |    \
            0-----1

    节点按照逆时针方向排列：

        0 -> 1 -> 2

    对应局部边编号约定：

        edge 0:
            (1, 2)
            即 vertex 0 所对的边

        edge 1:
            (2, 0)
            即 vertex 1 所对的边

        edge 2:
            (0, 1)
            即 vertex 2 所对的边

    也就是说 Triangle3 采用：

        local edge i
            =
        local vertex i 的对边

    这种编号方式对于后续：

        - 边界条件；
        - 有限元边积分；
        - 单元局部坐标；
        - 边法向；
        - DG / FEM；
        - 高阶 Triangle 单元；

    都比较方便。

    Parameters
    ----------
    points : array_like
        网格节点坐标。

        对二维平面网格：

            shape = (NN, 2)

        对嵌入三维空间中的三角形曲面网格：

            shape = (NN, 3)

    cells : array_like
        Triangle3 单元连接关系。

        shape：

            (NC, 3)
    """

    def __init__(
        self,
        points,
        cells,
    ):
        """
        初始化 Triangle3 网格。

        Parameters
        ----------
        points : array_like
            节点坐标。

        cells : array_like
            Triangle3 单元连接关系。
        """

        # ------------------------------------------------------------
        # 初始化通用 Mesh
        # ------------------------------------------------------------
        #
        # TriangleMesh 固定使用：
        #
        #     cell_type = "triangle3"
        #
        # 具体的：
        #
        #     节点数量检查
        #     Cell connectivity 检查
        #     MeshTopology
        #     Edge 构建
        #     边界识别
        #     面积计算
        #     网格质量
        #
        # 均由 Mesh 基类统一负责。
        #
        super().__init__(
            points,
            cells,
            "triangle3",
        )

    @classmethod
    def from_box(
        cls,
        box=(0.0, 1.0, 0.0, 1.0),
        nx=1,
        ny=1,
    ):
        """
        在二维矩形区域生成规则 Triangle3 网格。

        该方法是 ``generate_triangle_box`` 的便捷封装。

        实际规则三角网格生成算法位于：

            opencaxpy.mesh.generators.box2d

        Parameters
        ----------
        box : tuple[float, float, float, float]
            二维矩形区域：

                (
                    xmin,
                    xmax,
                    ymin,
                    ymax,
                )

        nx : int
            x 方向规则网格划分数量。

            x 方向节点数为：

                nx + 1

        ny : int
            y 方向规则网格划分数量。

            y 方向节点数为：

                ny + 1

        Returns
        -------
        TriangleMesh
            生成的规则 Triangle3 网格。

        Notes
        -----
        ``generate_triangle_box`` 首先将矩形区域划分成：

            nx * ny

        个规则四边形块。

        每一个四边形块：

            n3 -------- n2
            |         / |
            |       /   |
            |     /     |
            |   /       |
            | /         |
            n0 -------- n1

        沿：

            n0 -> n2

        对角线划分为两个 Triangle3：

            triangle 0:
                (n0, n1, n2)

            triangle 1:
                (n0, n2, n3)

        两个 Triangle3 都采用逆时针节点方向。

        因此总单元数量为：

            2 * nx * ny

        总节点数量为：

            (nx + 1) * (ny + 1)

        Examples
        --------
        >>> mesh = TriangleMesh.from_box(
        ...     box=(0.0, 2.0, 0.0, 1.0),
        ...     nx=4,
        ...     ny=2,
        ... )
        >>>
        >>> mesh.number_of_nodes()
        15
        >>>
        >>> mesh.number_of_cells()
        16
        """

        # ------------------------------------------------------------
        # 延迟导入 Generator
        # ------------------------------------------------------------
        #
        # TriangleMesh 只负责表示 Triangle3 Mesh。
        #
        # 规则矩形区域的 Triangle3 网格生成算法由：
        #
        #     generators/box2d.py
        #
        # 独立负责。
        #
        from .generators.box2d import generate_triangle_box

        # ------------------------------------------------------------
        # 生成 points + cells
        # ------------------------------------------------------------

        points, cells = generate_triangle_box(
            box=box,
            nx=nx,
            ny=ny,
        )

        # ------------------------------------------------------------
        # 创建 TriangleMesh
        # ------------------------------------------------------------

        return cls(
            points,
            cells,
        )
