"""Test 7: mesh + numerical solution + error order in one row."""

import numpy as np

from opencaxpy.visualization import (
    ConvergencePlot,
    Field,
    MeshPlot,
    Solution,
    SolutionPlot,
    show,
)
from demo_mesh import triangle_mesh


mesh = triangle_mesh()

x = mesh.points[:, 0]
y = mesh.points[:, 1]
u = np.sin(np.pi * x) * np.sin(np.pi * y)
displacement = np.column_stack([0.02 * x, -0.03 * x * (1.0 + y)])

solution = Solution()
solution.add_field(Field("u", u, location="point", kind="scalar"))
solution.add_field(
    Field(
        "displacement",
        displacement,
        location="point",
        kind="vector",
        components=("x", "y"),
    )
)

h = np.array([0.5, 0.25, 0.125, 0.0625], dtype=float)
error = 0.15 * h**2

show(
    [
        MeshPlot(mesh, title="Mesh"),
        SolutionPlot(
            mesh,
            solution,
            field="u",
            deformation="displacement",
            scale="auto",
            title="Numerical Solution",
        ),
        ConvergencePlot(
            h,
            error,
            label="L2 error",
            expected_order=2,
            title="Error Order",
        ),
    ],
    layout=(1, 3),
    title="OpenCAXPy Visualization v2.0",
)
