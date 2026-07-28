import numpy as np

from opencaxpy import MeshFactory


def test_triangle_rectangle():
    mesh = MeshFactory.triangle_rectangle(0, 1, 0, 1, 2, 2)
    assert mesh.num_nodes == 9
    assert mesh.num_cells == 8
    assert np.isclose(mesh.backend.to_numpy(mesh.measure("cell")).sum(), 1.0)


def test_quad_rectangle():
    mesh = MeshFactory.quad_rectangle(0, 2, 0, 1, 2, 1)
    assert mesh.num_nodes == 6
    assert mesh.num_cells == 2
    assert np.isclose(mesh.backend.to_numpy(mesh.measure("cell")).sum(), 2.0)


def test_tetra_box():
    mesh = MeshFactory.tetra_box(0, 1, 0, 1, 0, 1, 1, 1, 1)
    assert mesh.num_cells == 6
    assert np.isclose(mesh.backend.to_numpy(mesh.measure("cell")).sum(), 1.0)


def test_hexa_box_torch():
    mesh = MeshFactory.hexa_box(
        0, 1, 0, 1, 0, 1, 1, 1, 1,
        backend="torch", device="cpu",
    )
    assert mesh.backend.name == "torch"
    assert mesh.num_cells == 1
    assert np.isclose(
        mesh.backend.to_numpy(mesh.measure("cell")).sum(), 1.0
    )
