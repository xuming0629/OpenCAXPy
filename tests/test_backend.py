import numpy as np

from opencaxpy import MeshFactory, refine


def test_torch_generation_and_refinement():
    mesh = MeshFactory.triangle_rectangle(
        nx=1, ny=1, backend="torch", device="cpu"
    )
    result = refine(mesh, method="uniform")
    assert result.mesh.backend.name == "torch"
    assert np.isclose(
        result.mesh.backend.to_numpy(
            result.mesh.measure("cell")
        ).sum(),
        1.0,
    )
