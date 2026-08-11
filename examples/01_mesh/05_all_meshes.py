#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : mesh_summary_example.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy 基础 Mesh 类型统一统计测试
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
    IntervalMesh,
    TriangleMesh,
    QuadrangleMesh,
    TetrahedronMesh,
    HexahedronMesh,
)


def print_title(title: str):
    """打印分隔标题。"""
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def print_mesh_info(mesh):
    """
    打印单个 Mesh 的基础信息。

    Parameters
    ----------
    mesh : Mesh
        OpenCAXPy Mesh 对象。
    """

    print_title(f"{type(mesh).__name__} / {mesh.cell_type}")

    # ================================================================
    # 1. Summary
    # ================================================================

    print("[Summary]")

    for key, value in mesh.summary().items():
        print(f"{key:24s} = {value}")

    # ================================================================
    # 2. Points
    # ================================================================

    print()
    print("[Points]")

    print(
        "points.shape =",
        mesh.points.shape,
    )

    print("points =")

    print(mesh.points)

    # ================================================================
    # 3. Cells
    # ================================================================

    print()
    print("[Cells]")

    print(
        "cells.shape =",
        mesh.cells.shape,
    )

    print("cells =")

    print(mesh.cells)

    # ================================================================
    # 4. Global Edge
    # ================================================================

    print()
    print("[Edges]")

    edges = mesh.entity("edge")

    print(
        "number_of_edges =",
        mesh.number_of_edges(),
    )

    print("edges =")

    print(edges)

    # ================================================================
    # 5. Face
    # ================================================================

    print()
    print("[Faces]")

    print(
        "number_of_faces =",
        mesh.number_of_faces(),
    )

    # 1D Mesh 没有 Face。
    if mesh.topological_dimension >= 2:
        print("faces =")

        print(mesh.entity("face"))
    else:
        print("faces = []")

    # ================================================================
    # 6. Cell -> Edge
    # ================================================================

    print()
    print("[Cell -> Edge]")

    print(mesh.cell_to_edge())

    # ================================================================
    # 7. Edge -> Cell
    # ================================================================

    print()
    print("[Edge -> Cell]")

    print(mesh.edge_to_cell())

    # ================================================================
    # 8. Cell -> Face / Face -> Cell
    # ================================================================

    if mesh.topological_dimension >= 2:

        print()
        print("[Cell -> Face]")

        print(mesh.cell_to_face())

        print()
        print("[Face -> Cell]")

        print(mesh.face_to_cell())

    # ================================================================
    # 9. Boundary Node
    # ================================================================

    print()
    print("[Boundary Node]")

    boundary_nodes = mesh.boundary_node_index()

    print(
        "boundary_node_index =",
        boundary_nodes,
    )

    # ================================================================
    # 10. Boundary Edge
    # ================================================================

    print()
    print("[Boundary Edge]")

    boundary_edges = mesh.boundary_edge_index()

    print(
        "boundary_edge_index =",
        boundary_edges,
    )

    # ================================================================
    # 11. Boundary Face
    # ================================================================

    print()
    print("[Boundary Face]")

    boundary_faces = mesh.boundary_face_index()

    print(
        "boundary_face_index =",
        boundary_faces,
    )

    # ================================================================
    # 12. Boundary Facet
    # ================================================================

    print()
    print("[Boundary Facet]")

    print(
        "boundary_facet_index =",
        mesh.boundary_facet_index(),
    )

    # ================================================================
    # 13. Cell Measure
    # ================================================================

    print()
    print("[Cell Measure]")

    measure = mesh.entity_measure("cell")

    print(
        "measure =",
        measure,
    )

    print(
        "measure_sum =",
        float(measure.sum()),
    )

    # ================================================================
    # 14. Cell Quality
    # ================================================================

    print()
    print("[Cell Quality]")

    quality = mesh.cell_quality()

    print(
        "quality =",
        quality,
    )

    if quality.size:

        print(
            "quality_min =",
            float(quality.min()),
        )

        print(
            "quality_max =",
            float(quality.max()),
        )

        print(
            "quality_mean =",
            float(quality.mean()),
        )

    # ================================================================
    # 15. Cell Barycenter
    # ================================================================

    print()
    print("[Cell Barycenter]")

    print(mesh.entity_barycenter("cell"))


def main():
    # ================================================================
    # 创建基础 Mesh
    # ================================================================

    meshes = [
        # ------------------------------------------------------------
        # Line2
        # ------------------------------------------------------------
        IntervalMesh.from_interval(
            interval=(0.0, 1.0),
            n=4,
        ),
        # ------------------------------------------------------------
        # Triangle3
        # ------------------------------------------------------------
        TriangleMesh.from_box(
            box=(0.0, 1.0, 0.0, 1.0),
            nx=2,
            ny=2,
        ),
        # ------------------------------------------------------------
        # Quad4
        # ------------------------------------------------------------
        QuadrangleMesh.from_box(
            box=(0.0, 1.0, 0.0, 1.0),
            nx=2,
            ny=2,
        ),
        # ------------------------------------------------------------
        # Tetra4
        # ------------------------------------------------------------
        TetrahedronMesh.from_box(
            box=(0.0, 1.0, 0.0, 1.0, 0.0, 1.0),
            nx=1,
            ny=1,
            nz=1,
        ),
        # ------------------------------------------------------------
        # Hexa8
        # ------------------------------------------------------------
        HexahedronMesh.from_box(
            box=(0.0, 1.0, 0.0, 1.0, 0.0, 1.0),
            nx=1,
            ny=1,
            nz=1,
        ),
    ]

    # ================================================================
    # 逐个 Mesh 打印
    # ================================================================

    for mesh in meshes:
        print_mesh_info(mesh)


if __name__ == "__main__":
    main()
