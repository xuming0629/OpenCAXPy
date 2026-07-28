# OpenCAXPy Fifth-Stage Meshing

This release implements five capability layers:

1. Adaptive triangle refinement
   - longest-edge bisection
   - newest-vertex convention
   - marked-cell refinement
   - conformity propagation
   - parent/child mapping

2. Rich polygon domains
   - holes
   - outer and hole segment tags
   - named boundary tags
   - region points and region tags

3. Pluggable meshing backends
   - SciPy Delaunay
   - Triangle
   - MeshPy
   - Gmsh
   - TetGen

4. High-order mesh support
   - Triangle6
   - Quad8/Quad9
   - Tetra10
   - geometry projector protocol
   - circle/sphere/callable projectors

5. 3D and advanced meshing foundations
   - TetGen tetrahedral backend
   - size-field protocol
   - constant, distance, box and composite fields
   - boundary-layer options

Optional backends are imported lazily. The base package remains usable without
Triangle, MeshPy, Gmsh or TetGen installed.
