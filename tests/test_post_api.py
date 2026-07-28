import importlib.util
import pytest

from opencaxpy import MeshFactory


@pytest.mark.skipif(
    importlib.util.find_spec("matplotlib") is None,
    reason="matplotlib not installed",
)
def test_plot_api():
    mesh = MeshFactory.triangle_rectangle(nx=1, ny=1)
    axes = mesh.plot(show=False)
    assert axes is not None


def test_viewer_constructs_without_importing_vtk():
    mesh = MeshFactory.hexa_box(nx=1, ny=1, nz=1)
    viewer = mesh.viewer()
    assert viewer.mesh is mesh
