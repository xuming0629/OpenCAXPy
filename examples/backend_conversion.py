from opencaxpy import QuadMesh


numpy_mesh = QuadMesh(
    points=[
        [0.0, 0.0],
        [1.0, 0.0],
        [1.0, 1.0],
        [0.0, 1.0],
    ],
    cells=[[0, 1, 2, 3]],
    backend="numpy",
)

numpy_mesh.cell_data["material_id"] = [7]

torch_mesh = numpy_mesh.torch(device="cpu")
restored = torch_mesh.numpy()

print(numpy_mesh.backend.name)
print(torch_mesh.backend.name)
print(restored.backend.name)
print(restored.cell_data["material_id"])
