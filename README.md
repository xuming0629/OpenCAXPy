# OpenCAXPy v1.1

General computational engineering and CAX framework.

v1.1 is the first runnable implementation based on the frozen
**OpenCAXPy Architecture 1.0**.

Implemented main paths:

- backend / linalg
- mesh
- field / function space / DOF entity abstraction
- FEM form + integrator
- Poisson P1
- Truss2D
- Euler-Bernoulli Beam2D
- Timoshenko Beam2D
- multi-property materials
- sections
- Model / Problem
- assembly / solver / analysis
- field-based results
- post-processing extension
- FVM/FDM/fluid/electromagnetic/multiphysics extension points

Run:

```bash
pip install -e .[dev]
pytest -q
```


## Mesh Kernel and Visualization

v1.1 mesh layer now provides:

- generic node / edge / face / cell entity API
- lazy `MeshTopology`
- `cell_to_edge`, `cell_to_face`
- `edge_to_cell`, `face_to_cell`
- boundary node / edge / face extraction
- edge length, cell measure and barycenter
- lightweight cell-quality diagnostics
- Interval2 / Triangle3 / Quad4 / Tetra4 / Hexa8 mesh families
- 2D / 3D Matplotlib `MeshViewer`
- node / edge / face / cell numbering
- boundary visualization

Examples:

```bash
python examples/01_mesh/01_triangle_topology.py
python examples/01_mesh/02_quad_mesh.py
python examples/01_mesh/03_tetra_mesh.py
python examples/01_mesh/04_hexa_mesh.py
python examples/01_mesh/05_all_meshes.py
```


## VTK-native visualization

OpenCAXPy v1.1 now uses **VTK** as its visualization backend. Matplotlib is not
used by the mesh viewer.

Core bridge:

```python
from opencaxpy import to_vtk_unstructured_grid
vtk_grid = to_vtk_unstructured_grid(mesh)
```

Interactive viewer:

```python
from opencaxpy import VTKMeshViewer, VTKMeshViewerOptions

viewer = VTKMeshViewer(
    mesh,
    VTKMeshViewerOptions(
        show_surface=True,
        show_edges=True,
        show_nodes=True,
        show_node_ids=True,
        show_cell_ids=True,
    ),
)
viewer.show()
```

Off-screen rendering is also supported with `save_screenshot()`.
