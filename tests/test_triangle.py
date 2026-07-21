import numpy as np

from opencaxpy import CellType, rectangle_triangle


def test_triangle_mesh_counts_and_area():
    mesh = rectangle_triangle(0.0, 1.0, 0.0, 1.0, 2, 2, diagonal="right")

    assert mesh.cell_type == CellType.TRIANGLE3
    assert mesh.num_nodes == 9
    assert mesh.num_cells == 8
    assert np.isclose(mesh.total_measure(), 1.0)

    topo = mesh.topology
    assert topo.num_edges == 16
    assert topo.boundary_edges.shape[0] == 8
    assert topo.boundary_nodes.shape[0] == 8
    assert mesh.validate()["is_valid"]


def test_triangle3_to_triangle6():
    mesh = rectangle_triangle(0.0, 1.0, 0.0, 1.0, 1, 1, diagonal="right")
    mesh2 = mesh.to_order(2)

    assert mesh2.cell_type == CellType.TRIANGLE6
    assert mesh2.num_nodes == mesh.num_nodes + mesh.topology.num_edges
    assert mesh2.cells.shape == (2, 6)
    assert np.isclose(mesh2.total_measure(), 1.0)
