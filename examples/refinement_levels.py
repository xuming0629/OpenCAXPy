from opencaxpy import MeshFactory, refine


mesh = MeshFactory.triangle_rectangle(
    x_min=0.0,
    x_max=1.0,
    y_min=0.0,
    y_max=1.0,
    nx=1,
    ny=1,
    diagonal="right",
)

result = refine(
    mesh,
    method="uniform",
    levels=1,
)

refined = result.mesh
backend = refined.backend

print("original cells =", mesh.num_cells)
print("refined cells  =", refined.num_cells)
print("levels         =", result.levels)
print(
    "parent previous =",
    backend.to_numpy(result.parent_cell).tolist(),
)
print(
    "parent original =",
    backend.to_numpy(result.parent_cell_original).tolist(),
)

viewer = refined.viewer(
    show_nodes=True,
    show_edges=True,
    show_node_ids=True,
    show_edge_ids=True,
    show_cell_ids=True,
)
viewer.show()
