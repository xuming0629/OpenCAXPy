#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : triangle_topology_example.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : Triangle3 网格拓扑关系及 VTK 可视化测试
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from pathlib import Path
import sys

import numpy as np

# ====================================================================
# 项目路径
# ====================================================================

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


from opencaxpy import (
    TriangleMesh,
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
    # ================================================================
    # 1. 创建 Triangle3 网格
    # ================================================================

    mesh = TriangleMesh.from_box(
        box=(0.0, 2.0, 0.0, 1.0),
        nx=4,
        ny=2,
    )

    # ================================================================
    # 2. Mesh 基础信息
    # ================================================================

    print_title("Mesh Summary")

    summary = mesh.summary()

    for key, value in summary.items():
        print(f"{key:<24} = {value}")

    print()
    print("geometric_dimension   =", mesh.geometric_dimension)
    print("topological_dimension =", mesh.topological_dimension)

    # ================================================================
    # 3. Node
    # ================================================================

    print_title("Node / Point")

    print("number_of_nodes =", mesh.number_of_nodes())

    print()
    print("points =")
    print(mesh.points)

    # 节点编号 + 坐标
    print()
    print("Node details:")

    for node_id, point in enumerate(mesh.points):
        print(f"node {node_id:3d} : " f"{np.array2string(point, precision=4)}")

    # ================================================================
    # 4. Cell
    # ================================================================

    print_title("Cell")

    print("number_of_cells =", mesh.number_of_cells())

    print()
    print("cells =")
    print(mesh.cells)

    print()
    print("Cell details:")

    for cell_id, cell in enumerate(mesh.cells):
        print(f"cell {cell_id:3d} : " f"{cell}")

    # ================================================================
    # 5. Edge
    # ================================================================

    print_title("Global Edge")

    edges = mesh.entity("edge")

    print("number_of_edges =", mesh.number_of_edges())

    print()
    print("edges =")
    print(edges)

    print()
    print("Edge details:")

    for edge_id, edge in enumerate(edges):
        print(f"edge {edge_id:3d} : " f"{edge}")

    # ================================================================
    # 6. Face
    # ================================================================

    print_title("Face")

    faces = mesh.entity("face")

    print("number_of_faces =", mesh.number_of_faces())

    print()
    print("faces =")
    print(faces)

    print()
    print("Triangle3 是二维网格，因此：Face == Cell")

    # ================================================================
    # 7. Cell -> Edge
    # ================================================================

    print_title("Cell -> Edge")

    cell_to_edge = mesh.cell_to_edge()

    print("cell_to_edge =")
    print(cell_to_edge)

    print()
    print("Detailed Cell -> Edge:")

    for cell_id, edge_ids in enumerate(cell_to_edge):
        print(f"cell {cell_id:3d} " f"{mesh.cells[cell_id]} " f"-> edges {edge_ids}")

        for local_edge_id, global_edge_id in enumerate(edge_ids):
            print(
                f"    local edge {local_edge_id} "
                f"-> global edge {global_edge_id:3d} "
                f"{edges[global_edge_id]}"
            )

    # ================================================================
    # 8. Edge -> Cell
    # ================================================================

    print_title("Edge -> Cell")

    edge_to_cell = mesh.edge_to_cell()

    print("edge_to_cell =")
    print(edge_to_cell)

    print()
    print("Detailed Edge -> Cell:")

    for edge_id, cell_ids in enumerate(edge_to_cell):
        print(f"edge {edge_id:3d} " f"{edges[edge_id]} " f"-> cells {cell_ids}")

    # ================================================================
    # 9. Cell -> Face
    # ================================================================

    print_title("Cell -> Face")

    cell_to_face = mesh.cell_to_face()

    print("cell_to_face =")
    print(cell_to_face)

    # 对二维 Mesh：
    #
    #     cell i == face i
    #
    print()
    print("Detailed Cell -> Face:")

    for cell_id, face_ids in enumerate(cell_to_face):
        print(f"cell {cell_id:3d} " f"-> face {face_ids}")

    # ================================================================
    # 10. Face -> Cell
    # ================================================================

    print_title("Face -> Cell")

    face_to_cell = mesh.face_to_cell()

    print("face_to_cell =")
    print(face_to_cell)

    print()
    print("Detailed Face -> Cell:")

    for face_id, cell_ids in enumerate(face_to_cell):
        print(f"face {face_id:3d} " f"-> cells {cell_ids}")

    # ================================================================
    # 11. Boundary Node
    # ================================================================

    print_title("Boundary Node")

    boundary_nodes = mesh.boundary_node_index()

    print("boundary_node_index =")
    print(boundary_nodes)

    print()
    print("Boundary Node details:")

    for node_id in boundary_nodes:
        print(f"node {node_id:3d} : " f"{mesh.points[node_id]}")

    # ================================================================
    # 12. Boundary Edge
    # ================================================================

    print_title("Boundary Edge")

    boundary_edges = mesh.boundary_edge_index()

    print("boundary_edge_index =")
    print(boundary_edges)

    print()
    print("Boundary Edge details:")

    for edge_id in boundary_edges:
        print(f"edge {edge_id:3d} : " f"{edges[edge_id]}")

    # ================================================================
    # 13. Boundary Face
    # ================================================================

    print_title("Boundary Face")

    boundary_faces = mesh.boundary_face_index()

    print("boundary_face_index =")
    print(boundary_faces)

    print()
    print(
        "注意：当前 Mesh.boundary_face_index() 对二维网格返回所有 Cell，"
        "因为二维 Cell 本身就是 Face。"
    )

    # ================================================================
    # 14. Boundary Facet
    # ================================================================

    print_title("Boundary Facet")

    boundary_facets = mesh.boundary_facet_index()

    print("boundary_facet_index =")
    print(boundary_facets)

    print()
    print("TriangleMesh 的拓扑维度 TD = 2，因此：")
    print("Boundary Facet == Boundary Edge")

    # ================================================================
    # 15. Node / Edge / Cell barycenter
    # ================================================================

    print_title("Entity Barycenter")

    print("node barycenter =")
    print(mesh.entity_barycenter("node"))

    print()
    print("edge barycenter =")
    print(mesh.entity_barycenter("edge"))

    print()
    print("cell barycenter =")
    print(mesh.entity_barycenter("cell"))

    # ================================================================
    # 16. Edge Length
    # ================================================================

    print_title("Edge Length")

    edge_lengths = mesh.edge_length()

    print("edge_length =")
    print(edge_lengths)

    print()
    print("Detailed Edge Length:")

    for edge_id, length in enumerate(edge_lengths):
        print(f"edge {edge_id:3d} " f"{edges[edge_id]} " f"length = {length:.6f}")

    # ================================================================
    # 17. Cell Area
    # ================================================================

    print_title("Cell Measure / Area")

    cell_area = mesh.entity_measure("cell")

    print("cell area =")
    print(cell_area)

    print()
    print("Detailed Cell Area:")

    for cell_id, area in enumerate(cell_area):
        print(f"cell {cell_id:3d} " f"{mesh.cells[cell_id]} " f"area = {area:.6f}")

    print()
    print(
        "total area =",
        cell_area.sum(),
    )

    # ================================================================
    # 18. Cell Quality
    # ================================================================

    print_title("Cell Quality")

    quality = mesh.cell_quality()

    print("cell_quality =")
    print(quality)

    print()
    print("Detailed Cell Quality:")

    for cell_id, q in enumerate(quality):
        print(f"cell {cell_id:3d} " f"quality = {q:.6f}")

    # ================================================================
    # 19. Cell Coordinates
    # ================================================================

    print_title("Cell Coordinates")

    for cell_id in range(mesh.number_of_cells()):
        print(f"cell {cell_id:3d}:")
        print(mesh.cell_coordinates(cell_id))

    # ================================================================
    # 20. Triangle Local Topology
    # ================================================================

    print_title("Triangle3 Local Topology")

    descriptor = mesh.descriptor

    print(
        "cell_type   =",
        descriptor.name,
    )

    print(
        "dimension   =",
        descriptor.dimension,
    )

    print(
        "num_nodes   =",
        descriptor.num_nodes,
    )

    print()
    print("local_edges =")

    for local_edge_id, edge in enumerate(descriptor.local_edges):
        print(f"local edge {local_edge_id} " f"= {edge}")

    print()
    print("Triangle3 局部 Edge 编号规则：")

    print("edge 0 -> vertex 0 的对边")

    print("edge 1 -> vertex 1 的对边")

    print("edge 2 -> vertex 2 的对边")

    # ================================================================
    # 21. 完整 Cell 局部 / 全局拓扑关系
    # ================================================================

    print_title("Complete Cell Local / Global Topology")

    for cell_id in range(mesh.number_of_cells()):
        cell = mesh.cells[cell_id]

        edge_ids = cell_to_edge[cell_id]

        print()
        print(f"Cell {cell_id}")

        print(
            "  global vertices =",
            cell,
        )

        print("  coordinates =")

        print(mesh.points[cell])

        print("  local edges:")

        for local_edge_id, local_edge in enumerate(descriptor.local_edges):
            global_edge_id = edge_ids[local_edge_id]

            global_edge = edges[global_edge_id]

            local_global_nodes = cell[
                np.asarray(
                    local_edge,
                    dtype=int,
                )
            ]

            print(
                f"    local edge {local_edge_id}: "
                f"local nodes {local_edge} "
                f"-> cell global nodes "
                f"{local_global_nodes} "
                f"-> global edge {global_edge_id} "
                f"{global_edge}"
            )

    # ================================================================
    # 22. VTK Visualization
    # ================================================================

    print_title("VTK Visualization")

    viewer = VTKMeshViewer(
        mesh,
        VTKMeshViewerOptions(
            show_surface=True,
            show_edges=True,
            show_nodes=True,
            show_node_ids=True,
            show_cell_ids=True,
            title="Triangle3 Mesh",
        ),
    )

    viewer.show()


if __name__ == "__main__":
    main()
