#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : meshio_adapter_example.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : meshio -> OpenCAXPy Triangle3 Mesh 适配及 VTK 可视化示例
# @Company       : 2026 XuMing. All Rights Reserved.

meshio -> OpenCAXPy Mesh 测试示例。

运行前安装：

    pip install gmsh meshio

本示例数据链路：

    Gmsh
      ↓
    .msh 文件
      ↓
    meshio.read()
      ↓
    meshio.Mesh
      ↓
    from_meshio()
      ↓
    OpenCAXPy TriangleMesh
      ↓
    MeshTopology
      ↓
    VTKMeshViewer
"""

from pathlib import Path
import sys

import gmsh
import meshio

# ====================================================================
# 项目路径
# ====================================================================

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


from opencaxpy.mesh.adapters.meshio import from_meshio

from opencaxpy import (
    VTKMeshViewer,
    VTKMeshViewerOptions,
)


def print_title(title: str):
    """打印分隔标题。"""
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def create_test_mesh(filename):
    """
    使用 Gmsh 创建测试用二维 Triangle 网格文件。

    Parameters
    ----------
    filename : str | pathlib.Path
        输出的 Gmsh ``.msh`` 文件路径。

    Notes
    -----
    本函数只用于生成测试文件。

    真正测试的 Adapter 链路是：

        meshio.read()
            ↓
        from_meshio()
            ↓
        OpenCAXPy Mesh
    """

    # ================================================================
    # 1. 初始化 Gmsh
    # ================================================================

    gmsh.initialize()

    try:
        # ============================================================
        # 2. 创建 Gmsh Model
        # ============================================================

        gmsh.model.add("meshio_test")

        # ============================================================
        # 3. 创建单位矩形
        # ============================================================
        #
        # 几何区域：
        #
        #     x ∈ [0, 1]
        #     y ∈ [0, 1]
        #
        gmsh.model.occ.addRectangle(
            0.0,
            0.0,
            0.0,
            1.0,
            1.0,
        )

        # OCC 几何同步。
        gmsh.model.occ.synchronize()

        # ============================================================
        # 4. 设置网格尺寸
        # ============================================================

        gmsh.option.setNumber(
            "Mesh.MeshSizeMin",
            0.2,
        )

        gmsh.option.setNumber(
            "Mesh.MeshSizeMax",
            0.2,
        )

        # ============================================================
        # 5. 生成二维 Triangle 网格
        # ============================================================

        gmsh.model.mesh.generate(2)

        # ============================================================
        # 6. 写出 msh 文件
        # ============================================================

        gmsh.write(str(filename))

    finally:
        # 即使生成过程中发生异常，
        # 也确保 Gmsh 正常释放。
        gmsh.finalize()


def main():
    print_title("meshio Adapter Example")

    # =================================================================
    # 1. 创建输出目录
    # =================================================================

    output_dir = ROOT / "output"

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    msh_file = output_dir / "meshio_test.msh"

    # =================================================================
    # 2. 使用 Gmsh 创建测试网格文件
    # =================================================================

    print_title("Step 1 - Create Gmsh Mesh File")

    create_test_mesh(msh_file)

    print(
        "mesh file =",
        msh_file,
    )

    # =================================================================
    # 3. meshio 读取 msh 文件
    # =================================================================

    print_title("Step 2 - meshio.read()")

    meshio_mesh = meshio.read(msh_file)

    # -------------------------------------------------------------
    # meshio points
    # -------------------------------------------------------------

    print(
        "meshio points shape =",
        meshio_mesh.points.shape,
    )

    print()
    print("first 10 meshio points =")

    print(meshio_mesh.points[:10])

    # -------------------------------------------------------------
    # meshio cell blocks
    # -------------------------------------------------------------

    print()
    print("meshio cell blocks:")

    for block_id, block in enumerate(meshio_mesh.cells):
        print(f"block {block_id:2d}: " f"type = {block.type:<12s} " f"shape = {block.data.shape}")

    # =================================================================
    # 4. meshio.Mesh -> OpenCAXPy Mesh
    # =================================================================

    print_title("Step 3 - meshio -> OpenCAXPy")

    # -------------------------------------------------------------
    # 显式指定 triangle3
    # -------------------------------------------------------------
    #
    # Gmsh 生成的 msh 文件通常可能同时包含：
    #
    #     line
    #     triangle
    #
    # 因此不建议这里依赖自动判断，
    # 明确告诉 Adapter 提取 Triangle CellBlock。
    #
    mesh = from_meshio(
        meshio_mesh,
        cell_type="triangle3",
    )

    print(
        "mesh class =",
        type(mesh).__name__,
    )

    print(
        "cell_type =",
        mesh.cell_type,
    )

    # =================================================================
    # 5. OpenCAXPy Mesh Summary
    # =================================================================

    print_title("OpenCAXPy Mesh Summary")

    for key, value in mesh.summary().items():
        print(f"{key:24s} = {value}")

    # =================================================================
    # 6. Nodes
    # =================================================================

    print_title("Nodes")

    print(
        "number_of_nodes =",
        mesh.number_of_nodes(),
    )

    print()
    print("first 10 nodes =")

    print(mesh.points[:10])

    # =================================================================
    # 7. Cells
    # =================================================================

    print_title("Cells")

    print(
        "number_of_cells =",
        mesh.number_of_cells(),
    )

    print()
    print("first 10 cells =")

    print(mesh.cells[:10])

    # =================================================================
    # 8. Global Edges
    # =================================================================

    print_title("Global Edges")

    edges = mesh.entity("edge")

    print(
        "number_of_edges =",
        mesh.number_of_edges(),
    )

    print()
    print("first 20 edges =")

    print(edges[:20])

    # =================================================================
    # 9. Cell -> Edge
    # =================================================================

    print_title("Cell -> Edge")

    cell_to_edge = mesh.cell_to_edge()

    print("cell_to_edge =")

    print(cell_to_edge)

    # =================================================================
    # 10. Edge -> Cell
    # =================================================================

    print_title("Edge -> Cell")

    edge_to_cell = mesh.edge_to_cell()

    print("edge_to_cell =")

    print(edge_to_cell)

    # =================================================================
    # 11. Boundary Nodes
    # =================================================================

    print_title("Boundary Nodes")

    boundary_nodes = mesh.boundary_node_index()

    print("boundary_node_index =")

    print(boundary_nodes)

    # =================================================================
    # 12. Boundary Edges
    # =================================================================

    print_title("Boundary Edges")

    boundary_edges = mesh.boundary_edge_index()

    print("boundary_edge_index =")

    print(boundary_edges)

    print()
    print("Boundary Edge details:")

    for edge_id in boundary_edges:
        print(f"edge {edge_id:3d} = " f"{edges[edge_id]}")

    # =================================================================
    # 13. Boundary Facets
    # =================================================================

    print_title("Boundary Facets")

    print("boundary_facet_index =")

    print(mesh.boundary_facet_index())

    # TriangleMesh：
    #
    #     TD = 2
    #
    # 所以：
    #
    #     Boundary Facet == Boundary Edge
    #

    # =================================================================
    # 14. Cell Area
    # =================================================================

    print_title("Cell Area")

    areas = mesh.entity_measure("cell")

    print("first 10 cell areas =")

    print(areas[:10])

    print()
    print(
        "total area =",
        areas.sum(),
    )

    # 对单位矩形而言：
    #
    #     total area ≈ 1.0
    #

    # =================================================================
    # 15. Cell Quality
    # =================================================================

    print_title("Cell Quality")

    quality = mesh.cell_quality()

    print("first 10 cell quality =")

    print(quality[:10])

    if quality.size:
        print()
        print(
            "quality min  =",
            quality.min(),
        )

        print(
            "quality mean =",
            quality.mean(),
        )

        print(
            "quality max  =",
            quality.max(),
        )

    # =================================================================
    # 16. Cell Barycenter
    # =================================================================

    print_title("Cell Barycenter")

    barycenter = mesh.entity_barycenter("cell")

    print("first 10 cell barycenters =")

    print(barycenter[:10])

    # =================================================================
    # 17. Triangle Local / Global Edge Mapping
    # =================================================================

    print_title("Triangle Local / Global Edge Mapping")

    descriptor = mesh.descriptor

    max_cells = min(
        10,
        mesh.number_of_cells(),
    )

    for cell_id in range(max_cells):
        cell = mesh.cells[cell_id]

        global_edge_ids = cell_to_edge[cell_id]

        print()
        print(f"cell {cell_id}:")

        print(
            "  global nodes =",
            cell,
        )

        for local_edge_id, local_edge in enumerate(descriptor.local_edges):
            global_edge_id = global_edge_ids[local_edge_id]

            global_nodes = cell[list(local_edge)]

            print(
                f"  local edge {local_edge_id}: "
                f"{local_edge} "
                f"-> global nodes {global_nodes} "
                f"-> global edge "
                f"{global_edge_id} "
                f"{edges[global_edge_id]}"
            )

    # =================================================================
    # 18. VTK Visualization
    # =================================================================

    print_title("VTK Visualization")

    viewer = VTKMeshViewer(
        mesh,
        VTKMeshViewerOptions(
            show_surface=True,
            show_edges=True,
            show_nodes=True,
            show_node_ids=True,
            show_edge_ids=True,
            show_cell_ids=True,
            title="meshio Triangle3 Mesh",
        ),
    )

    viewer.show()


if __name__ == "__main__":
    main()
