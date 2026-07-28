import importlib.util

import pytest

from opencaxpy import TriangleMesh


@pytest.mark.skipif(
    importlib.util.find_spec("matplotlib") is None,
    reason="matplotlib is not installed",
)
def test_matplotlib_plot_returns_axes():
    mesh = TriangleMesh(
        [[0,0], [1,0], [0,1]],
        [[0,1,2]],
    )
    axes = mesh.plot(show=False)
    assert axes is not None
