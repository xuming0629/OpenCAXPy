#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OpenCAXPy Mesh refinement public API。"""

from .hexahedron import uniform_refine_hexahedron
from .octree import Octree, OctreeCell
from .quadrangle import uniform_refine_quadrangle
from .quadtree import Quadtree, QuadtreeCell
from .tetrahedron import uniform_refine_tetrahedron
from .triangle import bisect_triangle, uniform_refine_triangle


def uniform_refine(mesh, levels=1):
    """根据 Mesh.cell_type 分派到对应的一致加密算法。"""
    dispatch = {
        "triangle3": uniform_refine_triangle,
        "quad4": uniform_refine_quadrangle,
        "tetra4": uniform_refine_tetrahedron,
        "hexa8": uniform_refine_hexahedron,
    }
    try:
        func = dispatch[str(mesh.cell_type).lower()]
    except KeyError as exc:
        raise NotImplementedError(
            f"uniform refinement is not implemented for {mesh.cell_type!r}"
        ) from exc
    return func(mesh, levels=levels)


__all__ = [
    "uniform_refine",
    "bisect_triangle",
    "uniform_refine_triangle",
    "uniform_refine_quadrangle",
    "uniform_refine_tetrahedron",
    "uniform_refine_hexahedron",
    "QuadtreeCell",
    "Quadtree",
    "OctreeCell",
    "Octree",
]
