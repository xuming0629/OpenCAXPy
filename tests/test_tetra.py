import numpy as np

from opencaxpy import CellType, box_tetra


def test_tetra_mesh():
    mesh = box_tetra(0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1, 1, 1)

    assert mesh.cell_type == CellType.TETRA4
    assert mesh.num_nodes == 8
    assert mesh.num_cells == 6
    assert np.isclose(mesh.total_measure(), 1.0)
    assert mesh.topology.boundary_faces.shape[0] == 12
    assert mesh.validate()["is_valid"]


def test_tetra4_to_tetra10():
    mesh = box_tetra(0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1, 1, 1)
    mesh2 = mesh.to_order(2)

    assert mesh2.cell_type == CellType.TETRA10
    assert mesh2.cells.shape == (6, 10)
    assert mesh2.num_nodes == mesh.num_nodes + mesh.topology.num_edges
