import opencaxpy as ocx


mesh = ocx.rectangle_triangle(
    xmin=0.0,
    xmax=1.0,
    ymin=0.0,
    ymax=1.0,
    nx=4,
    ny=4,
)

print(mesh)
print("total area:", mesh.total_measure())
print("edges:", mesh.topology.num_edges)
print("boundary edges:", mesh.topology.boundary_edges.shape[0])
print("boundary nodes:", mesh.topology.boundary_nodes)

triangle6 = mesh.to_order(2)
print(triangle6)
