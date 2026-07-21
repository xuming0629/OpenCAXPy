import numpy as np

from opencaxpy import CellType, box_hexa


def test_hexa_mesh():
    mesh = box_hexa(0.0, 2.0, 0.0, 1.0, 0.0, 1.0, 2, 1, 1)

    assert mesh.cell_type == CellType.HEXA8
    assert mesh.num_cells == 2
    assert mesh.num_nodes == 12
    assert np.isclose(mesh.total_measure(), 2.0)
    assert mesh.topology.num_faces == 11
    assert mesh.topology.boundary_faces.shape[0] == 10
    assert mesh.validate()["is_valid"]
