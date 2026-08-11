import numpy as np
from opencaxpy import TriangleMesh, LagrangeSpace, BilinearForm, DiffusionIntegrator, DenseAssembler


def test_symmetry():
    m = TriangleMesh.from_box((0, 1, 0, 1), 2, 2)
    V = LagrangeSpace(m)
    A = DenseAssembler().assemble_bilinear(BilinearForm(V).add_integrator(DiffusionIntegrator()))
    assert np.allclose(A, A.T)
