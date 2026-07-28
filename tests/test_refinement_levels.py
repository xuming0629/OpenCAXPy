import numpy as np
import pytest

from opencaxpy import MeshFactory, refine


def _np(mesh, value):
    return mesh.backend.to_numpy(value)


def test_triangle_uniform_levels_two_and_original_parent_mapping():
    mesh = MeshFactory.triangle_rectangle(
        nx=1,
        ny=1,
        diagonal="left",
    )

    result = refine(mesh, method="uniform", levels=2)

    assert result.mesh.num_cells == 32
    assert result.levels == 2
    assert len(result.level_results) == 2

    parent_previous = _np(result.mesh, result.parent_cell)
    parent_original = _np(result.mesh, result.parent_cell_original)

    assert parent_previous.shape == (32,)
    assert parent_original.shape == (32,)
    assert set(parent_original.tolist()) == {0, 1}
    assert np.count_nonzero(parent_original == 0) == 16
    assert np.count_nonzero(parent_original == 1) == 16


def test_refine_levels_zero_is_identity():
    mesh = MeshFactory.triangle_rectangle(nx=1, ny=1)
    result = refine(mesh, levels=0)

    assert result.mesh is mesh
    assert result.levels == 0
    assert result.level_results == ()
    assert _np(mesh, result.parent_cell).tolist() == [0, 1]
    assert _np(mesh, result.parent_cell_original).tolist() == [0, 1]
    assert _np(mesh, result.child_local_id).tolist() == [0, 0]


def test_mesh_refine_levels_keyword():
    mesh = MeshFactory.quad_rectangle(nx=1, ny=1)
    result = mesh.refine(method="uniform", levels=2)
    assert result.mesh.num_cells == 16


def test_refine_rejects_invalid_levels():
    mesh = MeshFactory.triangle_rectangle(nx=1, ny=1)

    with pytest.raises(ValueError):
        refine(mesh, levels=-1)

    with pytest.raises(TypeError):
        refine(mesh, levels=1.5)
