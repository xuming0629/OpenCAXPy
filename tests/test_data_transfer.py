import numpy as np

from opencaxpy import MeshFactory, refine


def test_quad_data_transfer():
    mesh = MeshFactory.quad_rectangle(nx=1, ny=1)
    mesh.point_data["temperature"] = [0.0, 2.0, 4.0, 6.0]
    mesh.cell_data["material"] = [7]

    result = refine(mesh, method="uniform")
    values = result.mesh.backend.to_numpy(
        result.mesh.point_data["temperature"]
    )
    materials = result.mesh.backend.to_numpy(
        result.mesh.cell_data["material"]
    )

    assert len(values) == 9
    assert materials.tolist() == [7, 7, 7, 7]
