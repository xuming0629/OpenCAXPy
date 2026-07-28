import numpy as np

from opencaxpy import MeshFactory, refine


def _total_measure(mesh):
    return float(mesh.backend.to_numpy(mesh.measure("cell")).sum())


def test_triangle_uniform_and_bisection():
    mesh = MeshFactory.triangle_rectangle(nx=1, ny=1)
    uniform = refine(mesh, method="uniform")
    assert uniform.mesh.num_cells == 8
    assert np.isclose(_total_measure(uniform.mesh), 1.0)

    bisected = refine(mesh, method="longest_edge", marked_cells=[0])
    assert bisected.mesh.num_cells >= 3
    assert np.isclose(_total_measure(bisected.mesh), 1.0)


def test_quad_uniform():
    mesh = MeshFactory.quad_rectangle(nx=1, ny=1)
    result = refine(mesh, method="uniform")
    assert result.mesh.num_cells == 4
    assert result.mesh.num_nodes == 9
    assert np.isclose(_total_measure(result.mesh), 1.0)


def test_tetra_uniform():
    mesh = MeshFactory.tetra_box(nx=1, ny=1, nz=1)
    result = refine(mesh, method="uniform")
    assert result.mesh.num_cells == 48
    assert np.isclose(_total_measure(result.mesh), 1.0)


def test_hexa_uniform():
    mesh = MeshFactory.hexa_box(nx=1, ny=1, nz=1)
    result = refine(mesh, method="uniform")
    assert result.mesh.num_cells == 8
    assert result.mesh.num_nodes == 27
    assert np.isclose(_total_measure(result.mesh), 1.0)


def test_multilevel_uniform():
    mesh = MeshFactory.quad_rectangle(nx=1, ny=1)
    result = refine(mesh, method="uniform", levels=2)
    assert result.mesh.num_cells == 16
    assert np.isclose(_total_measure(result.mesh), 1.0)
