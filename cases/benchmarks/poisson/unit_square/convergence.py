import numpy as np
from opencaxpy import (
    TriangleMesh,
    LagrangeSpace,
    Field,
    Model,
    Problem,
    PoissonPhysics,
    SteadyAnalysis,
)


def src(x):
    return 2 * np.pi**2 * np.sin(np.pi * x[0]) * np.sin(np.pi * x[1])


for n in (4, 8, 16, 32):
    mesh = TriangleMesh.from_box((0, 1, 0, 1), n, n)
    p = Problem(Model(mesh=mesh))
    p.add_field(Field("u", LagrangeSpace(mesh)))
    r = SteadyAnalysis(p).solve_poisson("u", PoissonPhysics(1.0, src), 0.0)
    ue = np.sin(np.pi * mesh.points[:, 0]) * np.sin(np.pi * mesh.points[:, 1])
    print(n, np.sqrt(np.mean((r.field("u").values - ue) ** 2)))
