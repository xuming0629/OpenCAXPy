"""Test 5: cell scalar field, representative of element stress results."""

import numpy as np

from opencaxpy.visualization import Field, Solution, show_solution
from demo_mesh import triangle_mesh


mesh = triangle_mesh()

# One value per cell.
von_mises = np.array([85.0, 132.0, 104.0, 61.0], dtype=float)

solution = Solution().add_field(
    Field(
        name="von_mises",
        values=von_mises,
        location="cell",
        kind="scalar",
        unit="MPa",
    )
)

show_solution(
    mesh,
    solution,
    field="von_mises",
    title="Von Mises Stress",
)
