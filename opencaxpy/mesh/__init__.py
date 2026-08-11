#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""OpenCAXPy mesh public API."""

from .cell_type import CELL_TYPES, CellType, get_cell_type
from .factory import create_mesh
from .hexahedron import HexahedronMesh
from .interval import IntervalMesh
from .mesh import Mesh
from .quadrangle import QuadrangleMesh
from .tetrahedron import TetrahedronMesh
from .topology import MeshTopology
from .triangle import TriangleMesh

__all__ = [
    "CellType",
    "CELL_TYPES",
    "get_cell_type",
    "MeshTopology",
    "Mesh",
    "create_mesh",
    "IntervalMesh",
    "TriangleMesh",
    "QuadrangleMesh",
    "TetrahedronMesh",
    "HexahedronMesh",
]

from .refinement import (
    Octree,
    OctreeCell,
    Quadtree,
    QuadtreeCell,
    bisect_triangle,
    uniform_refine,
    uniform_refine_hexahedron,
    uniform_refine_quadrangle,
    uniform_refine_tetrahedron,
    uniform_refine_triangle,
)

__all__ += [
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
