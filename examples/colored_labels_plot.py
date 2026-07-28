from opencaxpy import MeshFactory

mesh = MeshFactory.quad_rectangle(
    nx=3,
    ny=2,
)

mesh.plot(
    show_nodes=True,
    show_boundary=True,
    show_node_ids=True,
    show_edge_ids=True,
    show_cell_ids=True,

    node_label_color=(0.95, 0.20, 0.15),
    edge_label_color=(0.10, 0.45, 0.95),
    cell_label_color=(0.10, 0.70, 0.25),

    title="OpenCAXPy colored entity labels",
)
