import numpy as np
from opencaxpy import (
    TriangleMesh,
    QuadrangleMesh,
    TetrahedronMesh,
    HexahedronMesh,
)

def test_quality_is_finite_and_positive():
    meshes = [
        TriangleMesh.from_box((0,1,0,1),2,2),
        QuadrangleMesh.from_box((0,1,0,1),2,2),
        TetrahedronMesh.unit_tetrahedron(),
        HexahedronMesh.from_box((0,1,0,1,0,1),1,1,1),
    ]

    for mesh in meshes:
        q = mesh.cell_quality()
        assert np.all(np.isfinite(q))
        assert np.all(q > 0)
        assert np.all(q <= 1.0 + 1e-12)
