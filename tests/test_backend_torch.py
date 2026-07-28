import importlib.util

import numpy as np
import pytest

from opencaxpy import TriangleMesh


torch_available = importlib.util.find_spec("torch") is not None


@pytest.mark.skipif(
    not torch_available,
    reason="PyTorch is not installed",
)
def test_torch_backend():
    import torch

    mesh = TriangleMesh(
        [[0, 0], [1, 0], [0, 1], [1, 1]],
        [[0, 1, 2], [1, 3, 2]],
        backend="torch",
        device="cpu",
    )

    assert isinstance(mesh.points, torch.Tensor)
    assert mesh.number_of_edges() == 5
    assert torch.allclose(
        mesh.measure("cell"),
        torch.tensor([0.5, 0.5], dtype=torch.float64),
    )


@pytest.mark.skipif(
    not torch_available,
    reason="PyTorch is not installed",
)
def test_backend_conversion_preserves_data():
    mesh = TriangleMesh(
        [[0, 0], [1, 0], [0, 1]],
        [[0, 1, 2]],
        backend="numpy",
    )
    mesh.point_data["value"] = [1.0, 2.0, 3.0]

    torch_mesh = mesh.torch(device="cpu")
    restored = torch_mesh.numpy()

    assert torch_mesh.backend.name == "torch"
    assert restored.backend.name == "numpy"
    assert np.allclose(
        restored.point_data["value"],
        [1.0, 2.0, 3.0],
    )
