from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from opencaxpy import TriangleMesh, VTKMeshViewer, VTKMeshViewerOptions
from opencaxpy.mesh import TriangleMesh

mesh = TriangleMesh.from_box(
    box=(0.0, 1.0, 0.0, 1.0),
    nx=2,
    ny=2,
)

print(mesh.summary())

print(
    "nodes =",
    mesh.number_of_nodes(),
)

print(
    "edges =",
    mesh.number_of_edges(),
)

print(
    "cells =",
    mesh.number_of_cells(),
)

print(
    "boundary nodes =",
    mesh.boundary_node_index(),
)

print(
    "boundary edges =",
    mesh.boundary_edge_index(),
)

print(
    "cell area =",
    mesh.entity_measure("cell"),
)


viewer = VTKMeshViewer(
    mesh,
    VTKMeshViewerOptions(
        show_surface=True,
        show_edges=True,
        show_nodes=True,
        show_node_ids=True,
        show_cell_ids=True,
        show_edge_ids=True,
        title="Triangle3 Mesh",
    ),
)
viewer.show()
