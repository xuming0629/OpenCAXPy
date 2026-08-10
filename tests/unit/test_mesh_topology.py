import numpy as np
from opencaxpy import (
    TriangleMesh,
    QuadrangleMesh,
    TetrahedronMesh,
    HexahedronMesh,
)

def test_triangle_topology():
    mesh = TriangleMesh.from_box((0,1,0,1),1,1)
    assert mesh.number_of_nodes() == 4
    assert mesh.number_of_cells() == 2
    assert mesh.number_of_edges() == 5
    assert len(mesh.boundary_edge_index()) == 4
    assert len(mesh.boundary_node_index()) == 4

def test_quad_topology():
    mesh = QuadrangleMesh.from_box((0,1,0,1),2,1)
    assert mesh.number_of_nodes() == 6
    assert mesh.number_of_cells() == 2
    assert mesh.number_of_edges() == 7
    assert len(mesh.boundary_edge_index()) == 6
    assert np.allclose(mesh.entity_measure("cell"), 0.5)

def test_tetra_topology():
    mesh = TetrahedronMesh.unit_tetrahedron()
    assert mesh.number_of_edges() == 6
    assert mesh.number_of_faces() == 4
    assert len(mesh.boundary_face_index()) == 4
    assert np.isclose(mesh.entity_measure("cell")[0], 1/6)

def test_hexa_topology_and_volume():
    mesh = HexahedronMesh.from_box((0,1,0,1,0,1),1,1,1)
    assert mesh.number_of_nodes() == 8
    assert mesh.number_of_edges() == 12
    assert mesh.number_of_faces() == 6
    assert mesh.number_of_cells() == 1
    assert len(mesh.boundary_face_index()) == 6
    assert np.isclose(mesh.entity_measure("cell")[0], 1.0)
