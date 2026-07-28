import numpy as np

from opencaxpy import TriangleMesh


def test_numpy_mesh_topology_and_geometry():
    mesh = TriangleMesh(
        [[0, 0], [1, 0], [0, 1], [1, 1]],
        [[0, 1, 2], [1, 3, 2]],
        backend="numpy",
    )

    assert mesh.backend.name == "numpy"
    assert mesh.number_of_edges() == 5
    assert mesh.connectivity("cell", "cell").to_lists() == [[1], [0]]
    assert len(mesh.topology.boundary_entity_ids("edge")) == 4
    assert np.allclose(mesh.measure("cell"), [0.5, 0.5])


def test_numpy_mesh_data_validation():
    mesh = TriangleMesh(
        [[0, 0], [1, 0], [0, 1]],
        [[0, 1, 2]],
    )

    mesh.point_data["temperature"] = [10.0, 20.0, 30.0]
    mesh.cell_data["material"] = [1]

    assert np.allclose(
        mesh.point_data["temperature"],
        [10.0, 20.0, 30.0],
    )
