"""Test 3: nodal scalar numerical solution."""

import numpy as np

from opencaxpy.visualization import Field, Solution, show_solution
from demo_mesh import triangle_mesh


mesh = triangle_mesh()

# A synthetic nodal scalar field. It is intentionally solver-independent.
x = mesh.points[:, 0]
y = mesh.points[:, 1]
u = np.sin(np.pi * x) * np.sin(np.pi * y)

solution = Solution().add_field(
    Field(
        name="u",
        values=u,
        location="point",
        kind="scalar",
    )
)

show_solution(
    mesh,
    solution,
    field="u",
    title="Numerical Solution u",
)
