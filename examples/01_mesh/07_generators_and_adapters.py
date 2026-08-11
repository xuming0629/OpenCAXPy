#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : generator_factory_vtk_example.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : Mesh Generator + Factory + VTK Adapter 示例
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from pathlib import Path
import sys

# ====================================================================
# 项目路径
# ====================================================================

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


from opencaxpy import (
    create_mesh,
    to_vtk_unstructured_grid,
)

from opencaxpy.mesh.generators import (
    generate_triangle_box,
)


def main():
    # ================================================================
    # 1. 使用 Generator 生成基础网格数据
    # ================================================================
    #
    # Generator 只负责：
    #
    #     points
    #     cells
    #
    # 不直接创建 Mesh。
    #
    points, cells = generate_triangle_box(
        box=(0.0, 2.0, 0.0, 1.0),
        nx=4,
        ny=2,
    )

    print("=" * 80)
    print("Generated Mesh Data")
    print("=" * 80)

    print()
    print("points.shape =", points.shape)
    print("cells.shape  =", cells.shape)

    print()
    print("points =")
    print(points)

    print()
    print("cells =")
    print(cells)

    # ================================================================
    # 2. 使用 Mesh Factory 创建 OpenCAXPy Mesh
    # ================================================================
    #
    # Factory 根据：
    #
    #     cell_type = "triangle3"
    #
    # 自动创建：
    #
    #     TriangleMesh
    #
    mesh = create_mesh(
        points,
        cells,
        "triangle3",
    )

    print()
    print("=" * 80)
    print("OpenCAXPy Mesh")
    print("=" * 80)

    # ------------------------------------------------------------
    # Mesh Summary
    # ------------------------------------------------------------

    for key, value in mesh.summary().items():
        print(f"{key:24s} = {value}")

    # ------------------------------------------------------------
    # Boundary
    # ------------------------------------------------------------

    print()
    print(
        "boundary nodes =",
        mesh.boundary_node_index(),
    )

    print(
        "boundary edges =",
        mesh.boundary_edge_index(),
    )

    # ------------------------------------------------------------
    # Topology
    # ------------------------------------------------------------

    print()
    print("cell_to_edge =")
    print(mesh.cell_to_edge())

    print()
    print("edge_to_cell =")
    print(mesh.edge_to_cell())

    # ================================================================
    # 3. OpenCAXPy Mesh -> vtkUnstructuredGrid
    # ================================================================
    #
    # VTK Adapter 位于 visualization 层。
    #
    # 它负责：
    #
    #     OpenCAXPy Mesh
    #
    #             ↓
    #
    #     vtkUnstructuredGrid
    #
    # VTK 主要用于：
    #
    #     - 网格显示；
    #     - Field 显示；
    #     - 后处理；
    #     - 截图；
    #     - ParaView / VTK 数据链路。
    #
    vtk_grid = to_vtk_unstructured_grid(mesh)

    # ================================================================
    # 4. 检查 VTK 数据
    # ================================================================

    print()
    print("=" * 80)
    print("VTK Unstructured Grid")
    print("=" * 80)

    print(
        "vtk class =",
        vtk_grid.GetClassName(),
    )

    print(
        "number of points =",
        vtk_grid.GetNumberOfPoints(),
    )

    print(
        "number of cells =",
        vtk_grid.GetNumberOfCells(),
    )

    # ================================================================
    # 5. 打印 VTK CellType
    # ================================================================

    print()
    print("VTK cell types:")

    for cell_id in range(vtk_grid.GetNumberOfCells()):
        print(f"cell {cell_id:3d} " f"-> vtk type " f"{vtk_grid.GetCellType(cell_id)}")


if __name__ == "__main__":
    main()
