#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : meshio.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : meshio.Mesh -> OpenCAXPy Mesh 适配器
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

import numpy as np

from ..factory import create_mesh

# ====================================================================
# meshio 单元类型 -> OpenCAXPy CellType 映射
# ====================================================================
#
# meshio 使用字符串表示不同的网格单元类型。
#
# 当前 OpenCAXPy Mesh Kernel 支持的基础一次单元包括：
#
#     meshio "line"        -> OpenCAXPy "line2"
#     meshio "triangle"    -> OpenCAXPy "triangle3"
#     meshio "quad"        -> OpenCAXPy "quad4"
#     meshio "tetra"       -> OpenCAXPy "tetra4"
#     meshio "hexahedron"  -> OpenCAXPy "hexa8"
#
# 后续可以继续扩展：
#
#     line3
#     triangle6
#     quad8
#     quad9
#     tetra10
#     hexa20
#     wedge6
#     pyramid5
#
MESHIO_CELL_TYPES = {
    "line": "line2",
    "triangle": "triangle3",
    "quad": "quad4",
    "tetra": "tetra4",
    "hexahedron": "hexa8",
}


def from_meshio(
    mesh,
    cell_type=None,
):
    """
    将 ``meshio.Mesh`` 转换为单一 CellType 的 OpenCAXPy Mesh。

    本函数负责：

        1. 获取 meshio.Mesh 中的节点坐标；
        2. 选择目标 cell block；
        3. 将 meshio cell type 映射为 OpenCAXPy CellType；
        4. 处理二维网格的坐标降维；
        5. 通过 ``create_mesh`` 创建标准 OpenCAXPy Mesh。

    Parameters
    ----------
    mesh :
        meshio.Mesh 对象。

        例如：

            import meshio

            mesh = meshio.read("example.msh")

    cell_type : str | None
        希望转换的 OpenCAXPy 单元类型。

        当前支持：

            "line2"
            "triangle3"
            "quad4"
            "tetra4"
            "hexa8"

        如果为 None，则要求 meshio.Mesh 中只有一个
        OpenCAXPy 当前支持的 cell block。

    Returns
    -------
    Mesh
        转换后的 OpenCAXPy Mesh。

        实际类型由 cell_type 决定，例如：

            IntervalMesh
            TriangleMesh
            QuadrangleMesh
            TetrahedronMesh
            HexahedronMesh

    Raises
    ------
    ValueError
        当：

            - cell_type 为 None，但存在零个或多个支持的 cell block；
            - 指定的单元类型在 meshio.Mesh 中不存在。

    KeyError
        当指定的 OpenCAXPy cell_type 当前不受支持时。

    Notes
    -----
    meshio 的 ``points`` 通常使用三维坐标形式：

        (x, y, z)

    即使二维网格也可能保存为：

        (x, y, 0)

    因此当所有 z 坐标均为 0 时，
    本函数会自动将坐标转换为二维：

        (x, y)
    """

    # =================================================================
    # 1. 获取 meshio 中所有 CellBlock
    # =================================================================

    # mesh.cells 是一个 CellBlock 列表。
    #
    # 例如一个 Gmsh 文件中可能同时包含：
    #
    #     line
    #     triangle
    #
    # 或者：
    #
    #     triangle
    #     tetra
    #
    # 因此这里不能默认 mesh.cells 只有一种单元。
    #
    blocks = list(mesh.cells)

    # =================================================================
    # 2. 确定目标 CellBlock
    # =================================================================

    if cell_type is None:
        # -------------------------------------------------------------
        # 自动选择
        # -------------------------------------------------------------
        #
        # 只筛选 OpenCAXPy 当前支持的 meshio CellBlock。
        #
        supported = [block for block in blocks if block.type in MESHIO_CELL_TYPES]

        # 当前自动模式只允许唯一一个支持的 CellBlock。
        #
        # 如果存在多个，例如：
        #
        #     line
        #     triangle
        #
        # 就必须由用户明确指定：
        #
        #     cell_type="triangle3"
        #
        if len(supported) != 1:
            raise ValueError(
                "cell_type must be specified when meshio mesh contains "
                "zero or multiple supported cell blocks"
            )

        block = supported[0]

        # meshio cell type -> OpenCAXPy cell type
        target_type = MESHIO_CELL_TYPES[block.type]

    else:
        # -------------------------------------------------------------
        # 用户指定 OpenCAXPy CellType
        # -------------------------------------------------------------

        target_type = str(cell_type).lower()

        # 根据 OpenCAXPy CellType 反查 meshio 类型。
        #
        # 例如：
        #
        #     "triangle3"
        #
        # ->
        #
        #     "triangle"
        #
        meshio_type = next(
            (
                meshio_name
                for meshio_name, opencax_type in MESHIO_CELL_TYPES.items()
                if opencax_type == target_type
            ),
            None,
        )

        # 当前不支持该 OpenCAXPy 单元类型。
        if meshio_type is None:
            raise KeyError(f"Unsupported OpenCAXPy cell type: " f"{target_type!r}")

        # 在 meshio.Mesh 中寻找对应 CellBlock。
        block = next(
            (block for block in blocks if block.type == meshio_type),
            None,
        )

        # meshio 中不存在用户指定的 CellBlock。
        if block is None:
            raise ValueError(f"meshio mesh has no " f"{meshio_type!r} cell block")

    # =================================================================
    # 3. 获取节点坐标
    # =================================================================

    points = np.asarray(
        mesh.points,
        dtype=float,
    )

    # =================================================================
    # 4. 二维网格坐标降维
    # =================================================================

    # meshio 经常将二维网格保存为：
    #
    #     [
    #         [x0, y0, 0],
    #         [x1, y1, 0],
    #         ...
    #     ]
    #
    # 如果：
    #
    #     points.shape == (NN, 3)
    #
    # 且全部：
    #
    #     z == 0
    #
    # 则转换为：
    #
    #     [
    #         [x0, y0],
    #         [x1, y1],
    #         ...
    #     ]
    #
    if (
        points.ndim == 2
        and points.shape[1] == 3
        and np.allclose(
            points[:, 2],
            0.0,
        )
    ):
        points = points[:, :2]

    # =================================================================
    # 5. 获取 Cell Connectivity
    # =================================================================

    # meshio CellBlock.data 本身已经使用从 0 开始的
    # 连续节点数组索引，因此不像 Gmsh Adapter 那样需要
    # 再做 node tag -> local id 重映射。
    #
    cells = np.asarray(
        block.data,
        dtype=int,
    )

    # =================================================================
    # 6. 创建标准 OpenCAXPy Mesh
    # =================================================================

    # 从这里开始，后续：
    #
    #     MeshTopology
    #     FEM
    #     VTKMeshViewer
    #     Solver
    #
    # 都只面对统一的 OpenCAXPy Mesh，
    # 不需要知道原始网格来自 meshio。
    #
    return create_mesh(
        points,
        cells,
        target_type,
    )
