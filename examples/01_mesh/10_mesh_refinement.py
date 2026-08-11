#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OpenCAXPy Mesh Refinement 示例。"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from opencaxpy import (
    HexahedronMesh,
    Octree,
    QuadrangleMesh,
    Quadtree,
    TetrahedronMesh,
    TriangleMesh,
    VTKMeshViewer,
    VTKMeshViewerOptions,
    bisect_triangle,
    uniform_refine,
)


def show(mesh, title):
    print("=" * 72)
    print(title)
    print("=" * 72)
    for key, value in mesh.summary().items():
        print(f"{key:24s} = {value}")
    VTKMeshViewer(
        mesh,
        VTKMeshViewerOptions(
            show_surface=True,
            show_edges=True,
            show_nodes=True,
            show_cell_ids=True,
            title=title,
        ),
    ).show()


def main():
    tri = TriangleMesh.from_box((0, 1, 0, 1), 1, 1)
    show(uniform_refine(tri), "Triangle3 Uniform 1 -> 4")

    tri2 = TriangleMesh.from_box((0, 1, 0, 1), 2, 2)
    show(bisect_triangle(tri2, marked_cells=[0]), "Triangle3 Local Bisection")

    quad = QuadrangleMesh.from_box((0, 1, 0, 1), 1, 1)
    show(uniform_refine(quad), "Quad4 Uniform 1 -> 4")

    tet = TetrahedronMesh.unit_tetrahedron()
    show(uniform_refine(tet), "Tetra4 Uniform 1 -> 8")

    hexa = HexahedronMesh.from_box((0, 1, 0, 1, 0, 1), 1, 1, 1)
    show(uniform_refine(hexa), "Hexa8 Uniform 1 -> 8")

    qtree = Quadtree((0, 1, 0, 1)).uniform_refine(1)
    qtree.refine([0])
    show(qtree.to_mesh(), "Quadtree Leaves")

    otree = Octree((0, 1, 0, 1, 0, 1)).uniform_refine(1)
    show(otree.to_mesh(), "Octree Leaves")


if __name__ == "__main__":
    main()
