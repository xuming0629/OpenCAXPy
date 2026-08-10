# OpenCAXPy Architecture 1.0

Top-level architecture is frozen for OpenCAXPy 1.x.

## Constitution

1. Geometry != Mesh
2. Mesh != FunctionSpace
3. Field != DOF
4. Physics != Discretization
5. Discretization != Solver
6. Material != Section
7. Model != Problem
8. Problem != Analysis
9. Analysis != Solver
10. Post != Visualization

## Stable pipeline

Geometry -> Mesh -> Field/FunctionSpace -> Physics -> Discretization
-> Assembly -> Linear Algebra -> Solver -> Analysis -> Result -> Post
