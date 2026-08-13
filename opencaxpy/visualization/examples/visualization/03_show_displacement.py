"""Test 4: displacement magnitude and deformed geometry."""

import numpy as np

from opencaxpy.visualization import Field, Solution, show_solution
from demo_mesh import triangle_mesh


mesh = triangle_mesh()

x = mesh.points[:, 0]
y = mesh.points[:, 1]
displacement = np.column_stack(
    [
        0.025 * x,
        -0.035 * x * (1.0 + 0.4 * y),
    ]
)

solution = Solution().add_field(
    Field(
        name="displacement",
        values=displacement,
        location="point",
        kind="vector",
        components=("x", "y"),
        unit="mm",
    )
)

show_solution(
    mesh,
    solution,
    fields=[
        ("displacement", "magnitude"),
        ("displacement", "x"),
        ("displacement", "y"),
    ],
    deformation="displacement",
    scale="auto",
    layout=(1, 3),
    title="Displacement Results",
)
