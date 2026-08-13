"""Non-interactive smoke test for Visualization v2.0.

Useful on CI/headless Linux. It creates PNG files and verifies convergence order.
"""

from pathlib import Path
import numpy as np

from opencaxpy.visualization import (
    ConvergencePlot,
    Field,
    MeshPlot,
    Solution,
    SolutionPlot,
    estimate_convergence_order,
    show,
    show_mesh,
    show_solution,
)
from demo_mesh import triangle_mesh


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

mesh = triangle_mesh()
x = mesh.points[:, 0]
y = mesh.points[:, 1]

solution = Solution()
solution.add_field(Field("u", np.sin(np.pi * x) * np.sin(np.pi * y)))
solution.add_field(
    Field(
        "displacement",
        np.column_stack([0.02 * x, -0.03 * x * (1.0 + y)]),
        kind="vector",
        components=("x", "y"),
    )
)
solution.add_field(
    Field(
        "von_mises",
        np.array([80.0, 120.0, 95.0, 60.0]),
        location="cell",
    )
)

show_mesh(
    mesh,
    title="Mesh",
    save_path=OUTPUT_DIR / "mesh.png",
    interactive=False,
)

show_solution(
    mesh,
    solution,
    field="u",
    save_path=OUTPUT_DIR / "solution_u.png",
    interactive=False,
)

show_solution(
    mesh,
    solution,
    field="von_mises",
    save_path=OUTPUT_DIR / "von_mises.png",
    interactive=False,
)

h = np.array([0.5, 0.25, 0.125, 0.0625])
error = 0.2 * h**2
result = estimate_convergence_order(h, error)
assert np.isclose(result.fitted_order, 2.0, atol=1.0e-12)

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
        ConvergencePlot(h, error, expected_order=2, title="Error Order"),
    ],
    layout=(1, 3),
    title="Visualization Smoke Test",
    save_path=OUTPUT_DIR / "dashboard.png",
    interactive=False,
)

for path in sorted(OUTPUT_DIR.glob("*.png")):
    if path.stat().st_size <= 0:
        raise RuntimeError(f"Empty output file: {path}")
    print(path)

print("Visualization v2.0 smoke test passed.")
