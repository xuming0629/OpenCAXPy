from opencaxpy import MeshFactory, refine

meshes = (
    MeshFactory.triangle_rectangle(nx=1, ny=1),
    MeshFactory.quad_rectangle(nx=1, ny=1),
    MeshFactory.tetra_box(nx=1, ny=1, nz=1),
    MeshFactory.hexa_box(nx=1, ny=1, nz=1),
)

for mesh in meshes:
    result = refine(mesh, method="uniform")
    print(
        mesh.cell_type.name,
        mesh.num_cells,
        "->",
        result.mesh.num_cells,
    )
