# Meshing architecture

The meshing module follows a mesh-object plus generator/algorithm architecture.

```text
mesh/                       stable data model
meshing/
├── domain.py               geometric domains
├── factory.py              unified public entry point
├── generators/             mesh creation backends
│   ├── base.py             MeshGenerator + registry
│   ├── structured.py       rectangle and box generators
│   ├── polygon.py          arbitrary polygon triangulation
│   └── special.py          disk and L-shaped meshes
└── algorithms/             transformations of existing meshes
    ├── refine.py           uniform refinement
    ├── high_order.py       linear -> quadratic conversion
    └── quality.py          quality metrics
```

## Extension contract

A new generator only needs to implement `MeshGenerator.generate()` and register
it with `GeneratorRegistry`. Existing `Mesh`, FEM, Solver, Post and IO modules do
not need modification.

## Planned backends

- Triangle / MeshPy constrained Delaunay
- Gmsh CAD and discrete geometry adapters
- TetGen tetrahedral generation
- advancing-front and frontal-Delaunay algorithms
- quadtree/octree and Cartesian cut-cell meshing
- boundary-layer and anisotropic metric meshing
- adaptive bisection, red-green and newest-vertex refinement
- curved high-order node projection to CAD or implicit boundaries
