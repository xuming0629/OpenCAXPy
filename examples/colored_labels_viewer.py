from opencaxpy import MeshFactory

mesh = MeshFactory.triangle_rectangle(
    nx=3,
    ny=2,
)

viewer = mesh.viewer(
    show_nodes=True,
    show_edges=True,
    show_boundary=True,

    show_node_ids=True,
    show_edge_ids=True,
    show_cell_ids=True,

    node_color=(0.90, 0.25, 0.18),
    edge_color=(0.15, 0.15, 0.18),
    boundary_color=(0.95, 0.45, 0.08),

    node_label_color=(0.95, 0.20, 0.15),
    edge_label_color=(0.10, 0.45, 0.95),
    cell_label_color=(0.10, 0.70, 0.25),

    node_label_font_size=16,
    edge_label_font_size=14,
    cell_label_font_size=15,
)

viewer.show()
