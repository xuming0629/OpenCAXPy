# OpenCAXPy Visualization v2.0

统一面向 Mesh / Solution / Convergence 的可视化层。

## 默认网格颜色（保持 v1.x）

- background: `(0.94, 0.94, 0.94)`
- node: `(0.90, 0.20, 0.18)`
- edge: `(0.12, 0.32, 0.58)`
- face: `(0.45, 0.68, 0.88)`
- cell/surface: `(0.55, 0.78, 0.58)`
- text: `(0.15, 0.15, 0.15)`

## Public API

```python
from opencaxpy.visualization import (
    show, show_mesh, show_solution, show_convergence,
    Field, Solution, MeshPlot, SolutionPlot, ConvergencePlot,
)
```

### Mesh

```python
show_mesh(mesh)
```

### Solution

```python
solution = Solution()
solution.add_field(Field("displacement", u, location="point", kind="vector", components=("x", "y")))
solution.add_field(Field("von_mises", vm, location="cell", kind="scalar", unit="MPa"))

show_solution(mesh, solution, field="displacement", component="magnitude")
show_solution(mesh, solution, field="von_mises", deformation="displacement", scale="auto")
```

### Multiple solution panels

```python
show_solution(
    mesh,
    solution,
    fields=[("displacement", "magnitude"), "von_mises"],
    deformation="displacement",
    scale="auto",
    layout=(1, 2),
)
```

### Mesh + solution + convergence in one row

```python
show([
    MeshPlot(mesh, title="Mesh"),
    SolutionPlot(mesh, solution, field="von_mises", deformation="displacement", scale="auto", title="Von Mises"),
    ConvergencePlot(h, error, expected_order=2, title="L2 Error"),
], layout=(1, 3))
```

If all panels are VTK plots, v2.0 uses one VTK window with multiple viewports. Mixed VTK/Matplotlib panels are composited through offscreen VTK rendering into a Matplotlib figure, which can also be saved as a report image.
