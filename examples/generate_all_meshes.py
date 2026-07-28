from opencaxpy import MeshFactory

meshes = {
    "triangle": MeshFactory.triangle_rectangle(nx=4, ny=3),
    "quad": MeshFactory.quad_rectangle(nx=4, ny=3),
    "tetra": MeshFactory.tetra_box(nx=2, ny=2, nz=2),
    "hexa": MeshFactory.hexa_box(nx=2, ny=2, nz=2),
}

for name, mesh in meshes.items():
    print(
        name,
        "nodes=", mesh.num_nodes,
        "cells=", mesh.num_cells,
        "measure=", mesh.backend.to_numpy(mesh.measure("cell")).sum(),
    )
