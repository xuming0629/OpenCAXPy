"""Test 8: 3-D tetrahedron mesh and 3-D scalar solution."""

import numpy as np

from opencaxpy.visualization import Field, MeshPlot, Solution, SolutionPlot, show
from demo_mesh import tetra_mesh


mesh = tetra_mesh()

temperature = np.array([20.0, 35.0, 50.0, 42.0], dtype=float)
solution = Solution().add_field(
    Field(
        "temperature",
        temperature,
        location="point",
        kind="scalar",
        unit="degC",
    )
)

show(
    [
        MeshPlot(mesh, title="3D Tetra Mesh"),
        SolutionPlot(mesh, solution, field="temperature", title="Temperature"),
    ],
    layout=(1, 2),
    title="3D Visualization",
)
