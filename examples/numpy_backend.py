import numpy as np

from opencaxpy import TriangleMesh


mesh = TriangleMesh(
    points=np.array(
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, 1.0],
        ]
    ),
    cells=np.array(
        [
            [0, 1, 2],
            [1, 3, 2],
        ]
    ),
    backend="numpy",
)

print("backend =", mesh.backend.name)
print("nodes   =", mesh.number_of_nodes())
print("edges   =", mesh.number_of_edges())
print("cells   =", mesh.number_of_cells())
print("area    =", mesh.measure("cell"))
print("c2e     =", mesh.connectivity("cell", "edge").to_lists())
print("e2c     =", mesh.connectivity("edge", "cell").to_lists())
print("boundary edges:")
print(mesh.boundary_entities("edge"))
