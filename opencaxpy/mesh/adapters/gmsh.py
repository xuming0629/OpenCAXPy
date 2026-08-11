#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : gmsh.py
# @Time          : 2026-08-11 10:43:35
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : Gmsh Python model -> OpenCAXPy Mesh 适配器
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

import numpy as np

from ..factory import create_mesh

# ====================================================================
# Gmsh 基础一次单元类型映射
# ====================================================================
#
# Gmsh 使用整数 type id 表示不同的有限元单元类型。
#
# 当前 OpenCAXPy Mesh Kernel 先支持基础一次单元：
#
#     Gmsh type 1 -> 2 节点线单元
#     Gmsh type 2 -> 3 节点三角形
#     Gmsh type 3 -> 4 节点四边形
#     Gmsh type 4 -> 4 节点四面体
#     Gmsh type 5 -> 8 节点六面体
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
GMSH_ELEMENT_TYPES = {
    1: "line2",
    2: "triangle3",
    3: "quad4",
    4: "tetra4",
    5: "hexa8",
}


def from_gmsh(
    model,
    cell_type=None,
    dim=-1,
    tag=-1,
):
    """
    将已经生成网格的 ``gmsh.model`` 转换为 OpenCAXPy Mesh。

    该函数负责：

        1. 从 Gmsh model 中获取节点；
        2. 获取指定维度 / 实体上的单元；
        3. 将 Gmsh element type 映射为 OpenCAXPy CellType；
        4. 将 Gmsh node tag 重映射为连续的 OpenCAXPy node id；
        5. 最终通过 ``create_mesh`` 创建标准 OpenCAXPy Mesh。

    Parameters
    ----------
    model :
        Gmsh Python API 中的 ``gmsh.model`` 对象。

        调用本函数前必须已经完成网格生成，例如：

            gmsh.model.mesh.generate(2)

        或：

            gmsh.model.mesh.generate(3)

    cell_type : str | None
        希望提取并转换的 OpenCAXPy 单元类型。

        例如：

            "line2"
            "triangle3"
            "quad4"
            "tetra4"
            "hexa8"

        如果为 None，则要求当前 Gmsh 选择范围内只有一种
        OpenCAXPy 支持的单元类型，否则无法自动判断目标类型。

    dim : int
        Gmsh 几何实体维度。

        默认：

            -1

        表示不限定维度。

        常用：

            1 -> curve / line
            2 -> surface
            3 -> volume

    tag : int
        Gmsh 几何实体 tag。

        默认：

            -1

        表示不限定具体实体。

    Returns
    -------
    Mesh
        转换后的 OpenCAXPy Mesh。

        实际返回类型由 ``cell_type`` 决定，例如：

            TriangleMesh
            QuadrangleMesh
            TetrahedronMesh
            HexahedronMesh

    Raises
    ------
    ValueError
        当：

            - Gmsh 中没有节点；
            - 未指定 cell_type，但存在多个支持的单元类型；
            - 指定的 cell_type 在 Gmsh 网格中不存在。

    KeyError
        当指定的 OpenCAXPy cell_type 当前不受支持时。

    Notes
    -----
    Gmsh 中的 node tag 不要求从 0 开始，也不保证连续。

    例如 Gmsh 可能给出：

        1
        5
        11
        23

    但 OpenCAXPy Mesh connectivity 使用连续数组下标：

        0
        1
        2
        3

    因此本函数会显式建立：

        gmsh node tag -> OpenCAXPy local node id

    的映射关系。
    """

    # =================================================================
    # 1. 获取 Gmsh 节点
    # =================================================================

    # getNodes() 返回：
    #
    #     node_tags:
    #         Gmsh 节点 tag。
    #
    #     coords:
    #         节点坐标，Gmsh 始终按照：
    #
    #             x0, y0, z0,
    #             x1, y1, z1,
    #             ...
    #
    #         的一维数组形式返回。
    #
    #     parametric_coords:
    #         参数空间坐标，这里暂时不使用。
    #
    node_tags, coords, _ = model.mesh.getNodes(
        dim=dim,
        tag=tag,
        includeBoundary=True,
    )

    # 转换为 NumPy 数组。
    node_tags = np.asarray(
        node_tags,
        dtype=np.int64,
    )

    # Gmsh 坐标统一按照三维形式返回，
    # 因此 reshape 为：
    #
    #     (number_of_nodes, 3)
    #
    coords = np.asarray(
        coords,
        dtype=float,
    ).reshape(-1, 3)

    # 没有节点时不能构造 Mesh。
    if len(node_tags) == 0:
        raise ValueError("Gmsh model contains no nodes")

    # =================================================================
    # 2. 建立 Gmsh node tag -> OpenCAXPy node id 映射
    # =================================================================

    # Gmsh node tag 并不保证连续。
    #
    # 例如：
    #
    #     node_tags = [1, 4, 7, 12]
    #
    # OpenCAXPy connectivity 则要求基于数组下标：
    #
    #     [0, 1, 2, 3]
    #
    # 因此建立：
    #
    #     1  -> 0
    #     4  -> 1
    #     7  -> 2
    #     12 -> 3
    #
    tag_to_local = {int(tag_value): i for i, tag_value in enumerate(node_tags)}

    # =================================================================
    # 3. 获取 Gmsh 单元
    # =================================================================

    # getElements() 返回：
    #
    #     element_types:
    #         Gmsh element type id。
    #
    #     element_tags:
    #         每个单元自身的 Gmsh tag。
    #
    #     element_node_tags:
    #         每种 element type 对应的节点连接关系。
    #
    element_types, _, element_node_tags = model.mesh.getElements(
        dim=dim,
        tag=tag,
    )

    # 保存当前选择范围内所有 OpenCAXPy 支持的单元类型。
    candidates = []

    for gmsh_type, conn in zip(
        element_types,
        element_node_tags,
    ):
        gmsh_type = int(gmsh_type)

        # 当前只保留 OpenCAXPy 已支持的基础一次单元。
        if gmsh_type in GMSH_ELEMENT_TYPES:
            candidates.append(
                (
                    gmsh_type,
                    np.asarray(
                        conn,
                        dtype=np.int64,
                    ),
                )
            )

    # =================================================================
    # 4. 确定目标 CellType
    # =================================================================

    if cell_type is None:
        # -------------------------------------------------------------
        # 自动判断
        # -------------------------------------------------------------
        #
        # 当没有显式指定 cell_type 时，
        # 当前选择范围必须只有一种支持的单元类型。
        #
        if len(candidates) != 1:
            raise ValueError(
                "cell_type must be specified when Gmsh selection "
                "contains zero or multiple supported element types"
            )

        gmsh_type, conn = candidates[0]

        target_type = GMSH_ELEMENT_TYPES[gmsh_type]

    else:
        # -------------------------------------------------------------
        # 用户显式指定目标类型
        # -------------------------------------------------------------

        target_type = str(cell_type).lower()

        # 根据 OpenCAXPy cell_type 反查 Gmsh type id。
        gmsh_type = next(
            (
                gmsh_id
                for gmsh_id, opencax_type in GMSH_ELEMENT_TYPES.items()
                if opencax_type == target_type
            ),
            None,
        )

        # 当前 OpenCAXPy 不支持该单元类型。
        if gmsh_type is None:
            raise KeyError(f"Unsupported OpenCAXPy cell type: " f"{target_type!r}")

        # 在 Gmsh 当前选择范围中寻找对应的 element block。
        pair = next(
            (item for item in candidates if item[0] == gmsh_type),
            None,
        )

        # 用户要求的 CellType 在当前 Gmsh 网格中不存在。
        if pair is None:
            raise ValueError(f"Gmsh model has no elements " f"for {target_type!r}")

        _, conn = pair

    # =================================================================
    # 5. 整理单元 Connectivity
    # =================================================================

    # 当前基础一次单元的节点数。
    num_nodes = {
        1: 2,  # line2
        2: 3,  # triangle3
        3: 4,  # quad4
        4: 4,  # tetra4
        5: 8,  # hexa8
    }[gmsh_type]

    # Gmsh connectivity 原本是一维数组，例如：
    #
    #     triangle:
    #
    #     [1, 2, 3, 3, 4, 5, ...]
    #
    # 转换为：
    #
    #     [
    #         [1, 2, 3],
    #         [3, 4, 5],
    #         ...
    #     ]
    #
    conn = conn.reshape(
        -1,
        num_nodes,
    )

    # ---------------------------------------------------------------
    # Gmsh node tag -> OpenCAXPy local node id
    # ---------------------------------------------------------------
    #
    # 例如：
    #
    #     Gmsh:
    #
    #         [10, 25, 31]
    #
    #     OpenCAXPy:
    #
    #         [0, 1, 2]
    #
    cells = np.vectorize(
        tag_to_local.__getitem__,
        otypes=[int],
    )(conn)

    # =================================================================
    # 6. 根据拓扑维度处理坐标
    # =================================================================

    # OpenCAXPy 对基础单元的拓扑维度定义。
    dimension = {
        "line2": 1,
        "triangle3": 2,
        "quad4": 2,
        "tetra4": 3,
        "hexa8": 3,
    }[target_type]

    # Gmsh 始终返回三维坐标：
    #
    #     (x, y, z)
    #
    # 如果当前是一维 / 二维网格，并且所有 z 坐标均为 0，
    # 则删除无意义的 z 维度。
    #
    # 例如：
    #
    #     triangle3:
    #
    #         (x, y, 0)
    #
    #     ->
    #
    #         (x, y)
    #
    if dimension < 3 and np.allclose(
        coords[:, 2],
        0.0,
    ):
        coords = coords[
            :,
            : max(1, dimension),
        ]

    # =================================================================
    # 7. 创建标准 OpenCAXPy Mesh
    # =================================================================

    # 后续 MeshTopology、FEM、VTK Viewer 等模块只需要
    # 面向 OpenCAXPy Mesh 工作，不需要关心网格来自 Gmsh。
    #
    return create_mesh(
        coords,
        cells,
        target_type,
    )
