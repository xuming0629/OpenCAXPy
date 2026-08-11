#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : quadrangle.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy Quad4 四边形网格
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

from .mesh import Mesh


class QuadrangleMesh(Mesh):
    """
    四节点四边形网格。

    QuadrangleMesh 是基于 ``quad4`` 单元类型的
    二维面网格实现。

    每个 Quad4 Cell 包含 4 个局部节点。

    OpenCAXPy 当前采用的局部节点编号约定：

        3 -------- 2
        |          |
        |          |
        |          |
        0 -------- 1

    节点按照逆时针方向排列：

        0 -> 1 -> 2 -> 3

    对应局部边：

        edge 0:
            (0, 1)

        edge 1:
            (1, 2)

        edge 2:
            (2, 3)

        edge 3:
            (3, 0)

    Parameters
    ----------
    points : array_like
        网格节点坐标。

        对二维平面 Quad4 网格：

            shape = (NN, 2)

        对嵌入三维空间中的 Quad4 Surface：

            shape = (NN, 3)

    cells : array_like
        Quad4 单元连接关系。

        shape：

            (NC, 4)
    """

    def __init__(
        self,
        points,
        cells,
    ):
        """
        初始化 Quad4 网格。

        Parameters
        ----------
        points : array_like
            网格节点坐标。

        cells : array_like
            Quad4 单元连接关系。
        """

        # ------------------------------------------------------------
        # 初始化通用 Mesh
        # ------------------------------------------------------------
        #
        # QuadrangleMesh 固定使用：
        #
        #     cell_type = "quad4"
        #
        # 具体的：
        #
        #     节点数量检查
        #     Connectivity 检查
        #     MeshTopology
        #     几何测度
        #     网格质量
        #
        # 均由 Mesh 基类统一处理。
        #
        super().__init__(
            points,
            cells,
            "quad4",
        )

    @classmethod
    def from_box(
        cls,
        box=(0.0, 1.0, 0.0, 1.0),
        nx=1,
        ny=1,
    ):
        """
        在二维矩形区域生成规则 Quad4 网格。

        该方法是 ``generate_quad_box`` 的便捷封装。

        实际规则网格生成算法位于：

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
            x 方向网格划分数量。

            x 方向节点数量为：

                nx + 1

        ny : int
            y 方向网格划分数量。

            y 方向节点数量为：

                ny + 1

        Returns
        -------
        QuadrangleMesh
            生成的规则 Quad4 网格。

        Notes
        -----
        每一个规则矩形区域直接生成一个 Quad4 Cell。

        例如：

            nx = 2
            ny = 2

        节点：

            6 -------- 7 -------- 8
            |          |          |
            |          |          |
            3 -------- 4 -------- 5
            |          |          |
            |          |          |
            0 -------- 1 -------- 2

        对应四个 Quad4：

            cell 0:
                (0, 1, 4, 3)

            cell 1:
                (1, 2, 5, 4)

            cell 2:
                (3, 4, 7, 6)

            cell 3:
                (4, 5, 8, 7)

        每个 Quad4 均按照逆时针方向排列。

        Examples
        --------
        >>> mesh = QuadrangleMesh.from_box(
        ...     box=(0.0, 2.0, 0.0, 1.0),
        ...     nx=4,
        ...     ny=2,
        ... )
        >>>
        >>> mesh.number_of_nodes()
        15
        >>>
        >>> mesh.number_of_cells()
        8
        """

        # ------------------------------------------------------------
        # 延迟导入 Generator
        # ------------------------------------------------------------
        #
        # QuadrangleMesh 只负责表示 Quad4 Mesh。
        #
        # 规则矩形网格生成算法由：
        #
        #     generators/box2d.py
        #
        # 独立负责。
        #
        from .generators.box2d import generate_quad_box

        # ------------------------------------------------------------
        # 生成 points + cells
        # ------------------------------------------------------------

        points, cells = generate_quad_box(
            box=box,
            nx=nx,
            ny=ny,
        )

        # ------------------------------------------------------------
        # 创建 QuadrangleMesh
        # ------------------------------------------------------------

        return cls(
            points,
            cells,
        )
