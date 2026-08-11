#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : tetrahedron.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy Tetra4 四面体网格
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

import numpy as np

from .mesh import Mesh


class TetrahedronMesh(Mesh):
    """
    四节点四面体网格。

    TetrahedronMesh 是基于 ``tetra4`` 单元类型的
    三维体网格实现。

    每个 Tetra4 Cell 包含 4 个局部节点。

    一个标准四面体可以表示为：

                 3
                 |
                 |
                 |
                 |
                 0 -------- 1
                /
               /
              2

    对应标准坐标：

        node 0:
            (0, 0, 0)

        node 1:
            (1, 0, 0)

        node 2:
            (0, 1, 0)

        node 3:
            (0, 0, 1)

    Parameters
    ----------
    points : array_like
        网格节点坐标。

        对 Tetra4 网格：

            shape = (NN, 3)

    cells : array_like
        Tetra4 单元连接关系。

        shape：

            (NC, 4)
    """

    def __init__(
        self,
        points,
        cells,
    ):
        """
        初始化 Tetra4 网格。

        Parameters
        ----------
        points : array_like
            节点坐标。

        cells : array_like
            Tetra4 单元连接关系。
        """

        # ------------------------------------------------------------
        # 初始化通用 Mesh
        # ------------------------------------------------------------
        #
        # TetrahedronMesh 固定使用：
        #
        #     cell_type = "tetra4"
        #
        # 具体的：
        #
        #     节点数量检查
        #     Cell connectivity 检查
        #     MeshTopology
        #     几何测度
        #     网格质量
        #
        # 均由 Mesh 基类统一处理。
        #
        super().__init__(
            points,
            cells,
            "tetra4",
        )

    @classmethod
    def unit_tetrahedron(cls):
        """
        创建标准单位 Tetra4 网格。

        标准单位四面体顶点为：

            node 0:
                (0, 0, 0)

            node 1:
                (1, 0, 0)

            node 2:
                (0, 1, 0)

            node 3:
                (0, 0, 1)

        对应单元：

            (0, 1, 2, 3)

        Returns
        -------
        TetrahedronMesh
            只包含一个 Tetra4 Cell 的标准单位四面体网格。

        Notes
        -----
        该标准四面体体积为：

            V = 1 / 6

        这个方法主要用于：

            - Mesh 基础测试；
            - Topology 测试；
            - Tetra4 几何计算测试；
            - Jacobian 测试；
            - 有限元形函数测试；
            - 数值积分测试；
            - 单元刚度矩阵测试。

        Examples
        --------
        >>> mesh = TetrahedronMesh.unit_tetrahedron()
        >>>
        >>> mesh.number_of_nodes()
        4
        >>>
        >>> mesh.number_of_cells()
        1
        """

        # ------------------------------------------------------------
        # 标准单位 Tetra4 节点
        # ------------------------------------------------------------

        points = np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=float,
        )

        # ------------------------------------------------------------
        # 单元连接关系
        # ------------------------------------------------------------

        cells = np.array(
            [
                [0, 1, 2, 3],
            ],
            dtype=int,
        )

        return cls(
            points,
            cells,
        )

    @classmethod
    def from_box(
        cls,
        box=(0.0, 1.0, 0.0, 1.0, 0.0, 1.0),
        nx=1,
        ny=1,
        nz=1,
    ):
        """
        在三维长方体区域生成规则 Tetra4 网格。

        该方法是 ``generate_tetra_box`` 的便捷封装。

        实际网格生成算法位于：

            opencaxpy.mesh.generators.box3d

        Parameters
        ----------
        box : tuple[float, float, float, float, float, float]
            三维长方体区域：

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
        TetrahedronMesh
            生成的规则 Tetra4 网格。

        Notes
        -----
        ``generate_tetra_box`` 首先构造规则 Hexa block，
        然后将每个 Hexa 沿主对角线：

            n0 -> n6

        分解成 6 个 Tetra4。

        因此总 Cell 数为：

            6 * nx * ny * nz

        Examples
        --------
        >>> mesh = TetrahedronMesh.from_box(
        ...     box=(0, 1, 0, 1, 0, 1),
        ...     nx=2,
        ...     ny=2,
        ...     nz=2,
        ... )
        >>>
        >>> mesh.number_of_cells()
        48
        """

        # ------------------------------------------------------------
        # 延迟导入 Generator
        # ------------------------------------------------------------
        #
        # TetrahedronMesh 只负责表示 Tetra4 Mesh。
        #
        # 规则长方体区域的四面体剖分算法由：
        #
        #     generators/box3d.py
        #
        # 独立负责。
        #
        from .generators.box3d import generate_tetra_box

        # ------------------------------------------------------------
        # 生成 points + cells
        # ------------------------------------------------------------

        points, cells = generate_tetra_box(
            box=box,
            nx=nx,
            ny=ny,
            nz=nz,
        )

        # ------------------------------------------------------------
        # 创建 TetrahedronMesh
        # ------------------------------------------------------------

        return cls(
            points,
            cells,
        )
