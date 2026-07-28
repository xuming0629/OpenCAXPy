import numpy as np

from opencaxpy import Mesh, QuadMesh


def test_quad_area_and_barycenter():
    mesh = QuadMesh(
        [[0, 0], [2, 0], [2, 1], [0, 1]],
        [[0, 1, 2, 3]],
    )

    assert np.allclose(mesh.measure("cell"), [2.0])
    assert np.allclose(
        mesh.entity_barycenter("cell"),
        [[1.0, 0.5]],
    )


def test_tetra_volume():
    mesh = Mesh(
        [
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ],
        [[0, 1, 2, 3]],
        "tetra4",
    )

    assert np.allclose(mesh.measure("cell"), [1.0 / 6.0])
