#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : hexahedron.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy Hexa8 六面体网格
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

from .mesh import Mesh


class HexahedronMesh(Mesh):
    """
    八节点六面体网格。

    HexahedronMesh 是基于 ``hexa8`` 单元类型的
    三维体网格实现。

    每个 Hexa8 Cell 包含 8 个局部节点。

    OpenCAXPy 当前采用的局部节点编号约定：

               7 -------- 6
              /|         /|
             / |        / |
            4 -------- 5  |
            |  |       |  |
            |  3 ------|--2
            | /        | /
            |/         |/
            0 -------- 1

    其中：

        bottom face:
            0, 1, 2, 3

        top face:
            4, 5, 6, 7

    Parameters
    ----------
    points : array_like
        网格节点坐标。

        shape:

            (NN, 3)

    cells : array_like
        Hexa8 单元连接关系。

        shape:

            (NC, 8)
    """

    def __init__(
        self,
        points,
        cells,
    ):
        """
        初始化 Hexa8 网格。

        Parameters
        ----------
        points : array_like
            节点坐标。

        cells : array_like
            Hexa8 单元连接关系。
        """
        super().__init__(
            points,
            cells,
            "hexa8",
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
        在三维长方体区域生成规则 Hexa8 网格。

        该方法只是 ``generate_hexa_box`` 的便捷封装。

        实际网格生成算法位于：

            opencaxpy.mesh.generators.box3d

        中。

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
            x 方向网格划分数量。

        ny : int
            y 方向网格划分数量。

        nz : int
            z 方向网格划分数量。

        Returns
        -------
        HexahedronMesh
            生成的规则 Hexa8 网格。

        Examples
        --------
        >>> mesh = HexahedronMesh.from_box(
        ...     box=(0, 2, 0, 1, 0, 1),
        ...     nx=2,
        ...     ny=1,
        ...     nz=1,
        ... )
        >>>
        >>> mesh.number_of_cells()
        2
        """

        # ------------------------------------------------------------
        # 延迟导入 Generator
        # ------------------------------------------------------------
        #
        # 将网格生成算法放在 generators/ 中，
        # 避免 HexahedronMesh 本身承担具体生成算法。
        #
        from .generators.box3d import generate_hexa_box

        # ------------------------------------------------------------
        # 生成 points + cells
        # ------------------------------------------------------------

        points, cells = generate_hexa_box(
            box=box,
            nx=nx,
            ny=ny,
            nz=nz,
        )

        # ------------------------------------------------------------
        # 创建 HexahedronMesh
        # ------------------------------------------------------------

        return cls(
            points,
            cells,
        )
