from opencaxpy import MeshFactory


mesh = MeshFactory.triangle_rectangle(
    nx=1,
    ny=1,
    diagonal="left",
)

points = mesh.backend.to_numpy(mesh.points)
cells = mesh.backend.to_numpy(mesh.cells)
edges = mesh.backend.to_numpy(mesh.entity("edge"))
cell2edge = mesh.connectivity("cell", "edge").to_lists()
signs = mesh.backend.to_numpy(mesh.cell_to_edge_sign())

print(mesh)
print("local numbering:", mesh.local_numbering())

for cell_id, cell in enumerate(cells):
    print(f"\ncell {cell_id}: cell2node={cell.tolist()}")
    for local_edge_id, (local_a, local_b) in enumerate(
        mesh.cell_type.local_edges
    ):
        global_edge_id = cell2edge[cell_id][local_edge_id]
        directed = (
            int(cell[local_a]),
            int(cell[local_b]),
        )
        print(
            f"  local edge {local_edge_id}, "
            f"opposite local node {local_edge_id}: "
            f"directed={directed}, "
            f"global edge {global_edge_id}={edges[global_edge_id].tolist()}, "
            f"sign={int(signs[cell_id, local_edge_id]):+d}"
        )
