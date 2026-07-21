import pytest

torch = pytest.importorskip("torch")

from opencaxpy import rectangle_triangle


def test_torch_cpu_backend():
    mesh = rectangle_triangle(
        0.0, 1.0, 0.0, 1.0, 2, 2,
        backend="torch",
        device="cpu",
    )

    assert isinstance(mesh.points, torch.Tensor)
    assert isinstance(mesh.cells, torch.Tensor)
    assert mesh.points.dtype == torch.float64
    assert mesh.cells.dtype == torch.int64
    assert mesh.topology.edges.device.type == "cpu"
    assert abs(mesh.total_measure() - 1.0) < 1e-12
