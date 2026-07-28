from opencaxpy import TriangleMesh


mesh = TriangleMesh(
    points=[
        [0.0, 0.0],
        [1.0, 0.0],
        [0.0, 1.0],
        [1.0, 1.0],
        [0.5, 0.0],
        [0.5, 0.5],
        [0.0, 0.5],
        [1.0, 0.5],
        [0.5, 1.0],
    ],
    cells=[
        [0, 1, 2, 4, 5, 6],
        [1, 3, 2, 7, 8, 5],
    ],
    cell_type="triangle6",
)

print("base edges:")
print(mesh.entity("edge"))

print("high-order edge nodes:")
print(mesh.topology.high_order_edge_nodes().to_lists())
