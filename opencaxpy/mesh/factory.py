#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : factory.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy Mesh 工厂
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

from .hexahedron import HexahedronMesh
from .interval import IntervalMesh
from .quadrangle import QuadrangleMesh
from .tetrahedron import TetrahedronMesh
from .triangle import TriangleMesh

# ====================================================================
# OpenCAXPy CellType -> Mesh 类型映射
# ====================================================================
#
# Mesh Factory 根据标准 cell_type 名称，
# 创建对应的具体 Mesh 对象。
#
# 当前支持：
#
#     line2       -> IntervalMesh
#     triangle3   -> TriangleMesh
#     quad4       -> QuadrangleMesh
#     tetra4      -> TetrahedronMesh
#     hexa8       -> HexahedronMesh
#
# 后续增加新的网格单元时，只需要：
#
#     1. 实现对应 Mesh 类型；
#     2. 在这里注册；
#     3. CellType 中定义对应拓扑信息。
#
# 例如未来：
#
#     triangle6
#     quad8
#     quad9
#     tetra10
#     hexa20
#     wedge6
#     pyramid5
#
_MESH_TYPES = {
    "line2": IntervalMesh,
    "triangle3": TriangleMesh,
    "quad4": QuadrangleMesh,
    "tetra4": TetrahedronMesh,
    "hexa8": HexahedronMesh,
}


def create_mesh(
    points,
    cells,
    cell_type,
):
    """
    根据 ``cell_type`` 创建对应的 OpenCAXPy Mesh。

    Parameters
    ----------
    points : array_like
        网格节点坐标。

        例如二维网格：

            shape = (NN, 2)

        三维网格：

            shape = (NN, 3)

    cells : array_like
        单元连接关系。

        例如 Triangle3：

            [
                [0, 1, 2],
                [0, 2, 3],
            ]

    cell_type : str
        OpenCAXPy 标准单元类型名称。

        当前支持：

            "line2"
            "triangle3"
            "quad4"
            "tetra4"
            "hexa8"

        名称不区分大小写。

    Returns
    -------
    Mesh
        对应的具体 Mesh 实例。

        例如：

            "line2"
                -> IntervalMesh

            "triangle3"
                -> TriangleMesh

            "quad4"
                -> QuadrangleMesh

            "tetra4"
                -> TetrahedronMesh

            "hexa8"
                -> HexahedronMesh

    Raises
    ------
    KeyError
        当指定的 ``cell_type`` 当前没有对应的 Mesh 类型时抛出。

    Examples
    --------
    创建 TriangleMesh：

        >>> mesh = create_mesh(
        ...     points,
        ...     cells,
        ...     "triangle3",
        ... )

    创建 TetrahedronMesh：

        >>> mesh = create_mesh(
        ...     points,
        ...     cells,
        ...     "tetra4",
        ... )

    Notes
    -----
    Mesh Factory 只负责：

        points + cells + cell_type
                    ↓
              Concrete Mesh

    不负责：

        - 网格生成；
        - Gmsh 调用；
        - meshio 文件读取；
        - VTK 可视化；
        - 网格拓扑计算。

    对应职责分别属于：

        generators/
            -> 网格生成

        adapters/
            -> 外部网格转换

        MeshTopology
            -> 拓扑关系

        visualization/
            -> VTK 可视化
    """

    # ------------------------------------------------------------
    # 标准化 CellType 名称
    # ------------------------------------------------------------

    key = str(cell_type).lower()

    # ------------------------------------------------------------
    # 查询具体 Mesh 类型
    # ------------------------------------------------------------

    try:
        mesh_cls = _MESH_TYPES[key]

    except KeyError as exc:
        raise KeyError(
            f"Unsupported mesh cell type {cell_type!r}. " f"Available: {tuple(_MESH_TYPES.keys())}"
        ) from exc

    # ------------------------------------------------------------
    # 创建具体 Mesh
    # ------------------------------------------------------------

    return mesh_cls(
        points,
        cells,
    )
