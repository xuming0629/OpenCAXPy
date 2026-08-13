# Visualization v2.0 Examples

Run these examples from the OpenCAXPy repository root after placing Visualization v2.0 under `opencaxpy/visualization`.

```bash
python examples/visualization/00_show_mesh.py
python examples/visualization/01_show_mesh_multiple.py
python examples/visualization/02_show_scalar_solution.py
python examples/visualization/03_show_displacement.py
python examples/visualization/04_show_cell_stress.py
python examples/visualization/05_show_convergence.py
python examples/visualization/06_show_dashboard.py
python examples/visualization/07_show_3d_tetra.py
```

For a non-interactive/headless test:

```bash
python examples/visualization/08_smoke_test.py
```

The smoke test writes PNG files to `examples/visualization/outputs/`.

## Coverage

- `00`: single 2-D mesh, nodes and IDs
- `01`: multiple mesh panels
- `02`: nodal scalar solution
- `03`: displacement vector components, magnitude and deformation
- `04`: cell scalar / element stress
- `05`: convergence curve and fitted error order
- `06`: mixed mesh + solution + convergence dashboard
- `07`: 3-D tetra mesh and scalar solution
- `08`: non-interactive regression/smoke test
