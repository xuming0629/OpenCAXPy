import numpy as np

from opencaxpy import CellType, rectangle_quad


def test_quad_mesh():
    mesh = rectangle_quad(0.0, 2.0, 0.0, 1.0, 2, 1)

    assert mesh.cell_type == CellType.QUAD4
    assert mesh.num_nodes == 6
    assert mesh.num_cells == 2
    assert mesh.topology.num_edges == 7
    assert mesh.topology.boundary_edges.shape[0] == 6
    assert np.isclose(mesh.total_measure(), 2.0)


def test_quad4_to_quad8_and_quad9():
    mesh = rectangle_quad(0.0, 1.0, 0.0, 1.0, 1, 1)
    q8 = mesh.to_order(2, quad_center=False)
    q9 = mesh.to_order(2, quad_center=True)

    assert q8.cell_type == CellType.QUAD8
    assert q8.cells.shape == (1, 8)
    assert q9.cell_type == CellType.QUAD9
    assert q9.cells.shape == (1, 9)
