#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : gmsh_adapter_example.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : Gmsh -> OpenCAXPy Triangle3 Mesh 适配及 VTK 可视化示例
# @Company       : 2026 XuMing. All Rights Reserved.

Gmsh -> OpenCAXPy Mesh 测试示例。

运行前安装：

    pip install gmsh

本示例完整数据链路：

    Gmsh Geometry
          ↓
    Gmsh Mesh
          ↓
    from_gmsh()
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

# ====================================================================
# 项目路径
# ====================================================================

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


from opencaxpy.mesh.adapters.gmsh import from_gmsh

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


def main():
    print_title("Gmsh Adapter Example")

    # =================================================================
    # 1. 初始化 Gmsh
    # =================================================================
    #
    # Gmsh Python API 在使用之前必须初始化。
    #
    # 建议始终使用：
    #
    #     gmsh.initialize()
    #
    #     try:
    #         ...
    #     finally:
    #         gmsh.finalize()
    #
    # 保证即使中间发生异常，也能够正常释放 Gmsh 资源。
    #
    gmsh.initialize()

    try:
        # =============================================================
        # 2. 创建 Gmsh Model
        # =============================================================

        gmsh.model.add("rectangle")

        # =============================================================
        # 3. 创建二维矩形几何
        # =============================================================
        #
        # 创建：
        #
        #     x ∈ [0, 2]
        #     y ∈ [0, 1]
        #
        # 的二维矩形区域。
        #
        # addRectangle 参数：
        #
        #     x
        #     y
        #     z
        #     dx
        #     dy
        #
        surface = gmsh.model.occ.addRectangle(
            0.0,
            0.0,
            0.0,
            2.0,
            1.0,
        )

        print(
            "Gmsh surface tag =",
            surface,
        )

        # -------------------------------------------------------------
        # OCC 几何同步
        # -------------------------------------------------------------
        #
        # 使用 gmsh.model.occ 创建几何后，
        # 必须 synchronize() 才能进入后续 Mesh 操作。
        #
        gmsh.model.occ.synchronize()

        # =============================================================
        # 4. 设置 Gmsh 网格尺寸
        # =============================================================

        gmsh.option.setNumber(
            "Mesh.MeshSizeMin",
            0.5,
        )

        gmsh.option.setNumber(
            "Mesh.MeshSizeMax",
            0.5,
        )

        # =============================================================
        # 5. 生成二维网格
        # =============================================================
        #
        # 参数 2 表示：
        #
        #     生成二维 Surface Mesh
        #
        # Gmsh 默认情况下会生成 Triangle 单元。
        #
        gmsh.model.mesh.generate(2)

        # =============================================================
        # 6. Gmsh -> OpenCAXPy
        # =============================================================
        #
        # from_gmsh() 内部负责：
        #
        #     Gmsh node tag
        #           ↓
        #     OpenCAXPy local node id
        #
        # 以及：
        #
        #     Gmsh Triangle
        #           ↓
        #     triangle3
        #
        mesh = from_gmsh(
            gmsh.model,
            cell_type="triangle3",
        )

        # =============================================================
        # 7. Mesh Summary
        # =============================================================

        print_title("OpenCAXPy Mesh Summary")

        for key, value in mesh.summary().items():
            print(f"{key:24s} = {value}")

        # =============================================================
        # 8. Node
        # =============================================================

        print_title("Nodes")

        print(
            "number_of_nodes =",
            mesh.number_of_nodes(),
        )

        print()
        print("points =")
        print(mesh.points)

        # =============================================================
        # 9. Cell
        # =============================================================

        print_title("Cells")

        print(
            "number_of_cells =",
            mesh.number_of_cells(),
        )

        print()
        print("first 10 cells =")
        print(mesh.cells[:10])

        # =============================================================
        # 10. Global Edge
        # =============================================================

        print_title("Edges")

        edges = mesh.entity("edge")

        print(
            "number_of_edges =",
            mesh.number_of_edges(),
        )

        print()
        print("first 20 edges =")
        print(edges[:20])

        # =============================================================
        # 11. Cell -> Edge
        # =============================================================

        print_title("Cell -> Edge")

        cell_to_edge = mesh.cell_to_edge()

        print("cell_to_edge =")

        print(cell_to_edge)

        # =============================================================
        # 12. Edge -> Cell
        # =============================================================

        print_title("Edge -> Cell")

        edge_to_cell = mesh.edge_to_cell()

        print("edge_to_cell =")

        print(edge_to_cell)

        # =============================================================
        # 13. Boundary Node
        # =============================================================

        print_title("Boundary Nodes")

        boundary_nodes = mesh.boundary_node_index()

        print("boundary_node_index =")

        print(boundary_nodes)

        # =============================================================
        # 14. Boundary Edge
        # =============================================================

        print_title("Boundary Edges")

        boundary_edges = mesh.boundary_edge_index()

        print("boundary_edge_index =")

        print(boundary_edges)

        print()
        print("Boundary Edge details:")

        for edge_id in boundary_edges:
            print(f"edge {edge_id:3d} = " f"{edges[edge_id]}")

        # =============================================================
        # 15. Boundary Facet
        # =============================================================
        #
        # 当前 TriangleMesh：
        #
        #     TD = 2
        #
        # 所以：
        #
        #     boundary facet == boundary edge
        #
        print_title("Boundary Facets")

        print("boundary_facet_index =")

        print(mesh.boundary_facet_index())

        # =============================================================
        # 16. Cell Area
        # =============================================================

        print_title("Cell Area")

        areas = mesh.entity_measure("cell")

        print("first 10 cell areas =")

        print(areas[:10])

        print()
        print(
            "total area =",
            areas.sum(),
        )

        # =============================================================
        # 17. Cell Quality
        # =============================================================

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

        # =============================================================
        # 18. Cell Barycenter
        # =============================================================

        print_title("Cell Barycenter")

        barycenter = mesh.entity_barycenter("cell")

        print("first 10 cell barycenters =")

        print(barycenter[:10])

        # =============================================================
        # 19. Local / Global Edge Mapping
        # =============================================================

        print_title("Triangle Local / Global Edge Mapping")

        descriptor = mesh.descriptor

        # 为了避免输出过多，
        # 这里只打印前 10 个 Cell。
        #
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

        # =============================================================
        # 20. VTK Visualization
        # =============================================================

        print_title("VTK Visualization")

        viewer = VTKMeshViewer(
            mesh,
            VTKMeshViewerOptions(
                show_surface=True,
                show_edges=True,
                show_nodes=True,
                # 显示各种拓扑实体编号。
                show_node_ids=True,
                show_edge_ids=True,
                show_cell_ids=True,
                title="Gmsh Triangle3 Mesh",
            ),
        )

        viewer.show()

    finally:
        # =============================================================
        # 21. 释放 Gmsh
        # =============================================================
        #
        # 即使：
        #
        #     from_gmsh()
        #     MeshTopology
        #     VTK Viewer
        #
        # 中任何步骤出现异常，也应该释放 Gmsh。
        #
        gmsh.finalize()


if __name__ == "__main__":
    main()
