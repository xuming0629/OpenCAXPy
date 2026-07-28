from opencaxpy import MeshFactory, refine

mesh = MeshFactory.hexa_box(nx=2, ny=2, nz=2)
mesh.cell_data["cell_id"] = list(range(mesh.num_cells))

refined = refine(mesh, method="uniform").mesh

viewer = mesh.viewer(
    show_nodes=True,
    show_edges=True,
    show_boundary=True,

    show_node_ids=True,
    show_edge_ids=True,
    show_cell_ids=True,

    node_label_color=(0.95, 0.20, 0.15),
    edge_label_color=(0.10, 0.45, 0.95),
    cell_label_color=(0.10, 0.70, 0.25),

    node_label_font_size=16,
    edge_label_font_size=14,
    cell_label_font_size=15,
)

viewer.show()