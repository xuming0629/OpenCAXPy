from opencaxpy import TriangleMesh


mesh = TriangleMesh(
    points=[
        [0.0, 0.0],
        [1.0, 0.0],
        [0.0, 1.0],
        [1.0, 1.0],
    ],
    cells=[
        [0, 1, 2],
        [1, 3, 2],
    ],
    backend="torch",
    device="cpu",
)

print("backend =", mesh.backend.name)
print("device  =", mesh.device)
print("points type =", type(mesh.points))
print("area =", mesh.measure("cell"))
print("edges =", mesh.entity("edge"))
