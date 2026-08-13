# Visualization v2.0: MeshStyle migration

## Public mesh API

```python
from opencaxpy.visualization import MeshStyle, show_mesh

style = MeshStyle(
    show_surface=True,
    show_edges=True,
    show_nodes=True,
    show_node_ids=True,
    show_edge_ids=True,
    show_cell_ids=True,
)

show_mesh(mesh, style=style, title="Triangle3 Mesh")
```

## Removed from the v2 public API

- `VTKMeshViewer`
- `VTKMeshViewerOptions`

`to_vtk_unstructured_grid` remains an internal visualization/backend adapter and should not be exported from `opencaxpy`.

## Responsibility split

- `MeshStyle`: mesh rendering style only.
- `MeshPlot.title` / `show_mesh(title=...)`: subplot title.
- `FigureOptions`: window size, figure size, DPI and whole-figure title.
- `FieldStyle`: solution field rendering.
- `DeformationStyle`: deformation rendering.
