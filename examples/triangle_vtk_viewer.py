# from opencaxpy import MeshFactory, refine


# def to_numpy(mesh, value):
#     """兼容 NumPy / PyTorch 双后端。"""
#     return mesh.backend.to_numpy(value)


# def print_connectivity(mesh, source: str, target: str) -> None:
#     connectivity = mesh.connectivity(source, target)

#     print(f"\n--- {source}2{target} ---")

#     for entity_id, related_ids in enumerate(connectivity.to_lists()):
#         print(f"{entity_id}: {related_ids}")


# def print_mesh_info(mesh, name: str = "mesh") -> None:
#     print("\n" + "=" * 70)
#     print(f"{name}")
#     print("=" * 70)

#     print(f"backend                = {mesh.backend.name}")
#     print(f"device                 = {mesh.device}")
#     print(f"cell type              = {mesh.cell_type.name}")
#     print(f"geometric dimension    = {mesh.geometric_dimension}")
#     print(f"topological dimension  = {mesh.topological_dimension}")
#     print(f"order                  = {mesh.order}")

#     print(f"num nodes              = {mesh.num_nodes}")
#     print(f"num edges              = {mesh.number_of_edges()}")
#     print(f"num cells              = {mesh.num_cells}")

#     print("\n--- points ---")
#     points = to_numpy(mesh, mesh.points)

#     for node_id, point in enumerate(points):
#         print(f"{node_id}: {point.tolist()}")

#     print("\n--- cells ---")
#     cells = to_numpy(mesh, mesh.cells)

#     for cell_id, cell in enumerate(cells):
#         print(f"{cell_id}: {cell.tolist()}")

#     print("\n--- edges ---")
#     edges = to_numpy(mesh, mesh.entity("edge"))

#     for edge_id, edge in enumerate(edges):
#         print(f"{edge_id}: {edge.tolist()}")

#     print("\n--- boundary edges ---")
#     boundary_edges = to_numpy(
#         mesh,
#         mesh.boundary_entities("edge"),
#     )

#     for boundary_id, edge in enumerate(boundary_edges):
#         print(f"{boundary_id}: {edge.tolist()}")

#     print("\n--- cell measures ---")
#     measures = to_numpy(mesh, mesh.measure("cell"))

#     for cell_id, measure in enumerate(measures):
#         print(f"{cell_id}: {float(measure)}")

#     print("\n--- cell barycenters ---")
#     barycenters = to_numpy(
#         mesh,
#         mesh.entity_barycenter("cell"),
#     )

#     for cell_id, center in enumerate(barycenters):
#         print(f"{cell_id}: {center.tolist()}")

#     print_connectivity(mesh, "cell", "node")
#     print_connectivity(mesh, "cell", "edge")
#     print_connectivity(mesh, "edge", "cell")
#     print_connectivity(mesh, "node", "cell")
#     print_connectivity(mesh, "cell", "cell")

#     print("\n--- point data ---")
#     if not mesh.point_data:
#         print("empty")
#     else:
#         for name, values in mesh.point_data.items():
#             print(
#                 f"{name}: "
#                 f"{to_numpy(mesh, values).tolist()}"
#             )

#     print("\n--- cell data ---")
#     if not mesh.cell_data:
#         print("empty")
#     else:
#         for name, values in mesh.cell_data.items():
#             print(
#                 f"{name}: "
#                 f"{to_numpy(mesh, values).tolist()}"
#             )


# def print_refinement_result(result) -> None:
#     mesh = result.mesh

#     print("\n" + "=" * 70)
#     print("refinement result")
#     print("=" * 70)

#     print(
#         "parent_cell =",
#         to_numpy(mesh, result.parent_cell).tolist(),
#     )

#     print(
#         "child_local_id =",
#         to_numpy(mesh, result.child_local_id).tolist(),
#     )

#     if result.old_to_new_node is not None:
#         print(
#             "old_to_new_node =",
#             to_numpy(mesh, result.old_to_new_node).tolist(),
#         )

#     if result.refined_cells is not None:
#         print(
#             "refined_cells =",
#             to_numpy(mesh, result.refined_cells).tolist(),
#         )

#     print("\n--- new node parent entities ---")

#     if not result.new_node_parent_entity:
#         print("empty")
#     else:
#         for record in result.new_node_parent_entity:
#             print(record)


# mesh = MeshFactory.triangle_rectangle(
#     x_min=0.0,
#     x_max=1.0,
#     y_min=0.0,
#     y_max=1.0,
#     nx=1,
#     ny=1,
#     diagonal="left",
# )

# mesh.cell_data["cell_id"] = list(
#     range(mesh.num_cells)
# )

# result = refine(
#     mesh,
#     method="uniform",
# )

# refined = result.mesh

# print_mesh_info(
#     mesh,
#     name="original triangle mesh",
# )

# print_refinement_result(result)

# print_mesh_info(
#     refined,
#     name="refined triangle mesh",
# )

# viewer = refined.viewer(
#     show_nodes=True,
#     show_edges=True,
#     show_boundary=False,

#     show_node_ids=True,
#     show_edge_ids=True,
#     show_cell_ids=True,

#     node_label_color=(0.95, 0.20, 0.15),
#     edge_label_color=(0.10, 0.45, 0.95),
#     cell_label_color=(0.10, 0.70, 0.25),

#     node_label_font_size=16,
#     edge_label_font_size=14,
#     cell_label_font_size=15,
# )

# viewer.show()


from __future__ import annotations

from opencaxpy import MeshFactory, refine


def to_numpy(mesh, value):
    """兼容 NumPy / PyTorch 双后端。"""
    return mesh.backend.to_numpy(value)


def print_connectivity(
    mesh,
    source: str,
    target: str,
) -> None:
    """
    打印普通拓扑连接关系。
    """
    connectivity = mesh.connectivity(
        source,
        target,
    )

    print(f"\n--- {source}2{target} ---")

    for entity_id, related_ids in enumerate(
        connectivity.to_lists()
    ):
        print(f"{entity_id}: {related_ids}")


def print_cell2edge_detail(mesh) -> None:
    """
    详细打印：

    1. 单元局部节点；
    2. 单元局部边；
    3. 局部边对应的全局边编号；
    4. 局部边方向；
    5. 全局边规范方向；
    6. 局部边与全局边的方向符号。
    """
    cells = to_numpy(
        mesh,
        mesh.cells,
    )

    edges = to_numpy(
        mesh,
        mesh.entity("edge"),
    )

    cell2edge = mesh.connectivity(
        "cell",
        "edge",
    ).to_lists()

    local_edges = mesh.cell_type.local_edges

    print("\n--- cell2edge detail ---")

    for cell_id, cell in enumerate(cells):
        print(
            f"\ncell {cell_id}: "
            f"nodes={cell.tolist()}"
        )

        global_edge_ids = cell2edge[cell_id]

        for local_edge_id, global_edge_id in enumerate(
            global_edge_ids
        ):
            local_node0, local_node1 = (
                local_edges[local_edge_id]
            )

            global_node0 = int(
                cell[local_node0]
            )

            global_node1 = int(
                cell[local_node1]
            )

            oriented_edge = (
                global_node0,
                global_node1,
            )

            canonical_edge = tuple(
                int(value)
                for value in edges[global_edge_id]
            )

            sign = (
                1
                if oriented_edge == canonical_edge
                else -1
            )

            print(
                f"  local edge {local_edge_id}: "
                f"local nodes=({local_node0}, {local_node1}), "
                f"oriented={oriented_edge}, "
                f"global edge={global_edge_id}, "
                f"canonical={canonical_edge}, "
                f"sign={sign:+d}"
            )


def print_mesh_info(
    mesh,
    name: str = "mesh",
) -> None:
    """
    打印网格的几何、拓扑和数据结构。
    """
    print("\n" + "=" * 78)
    print(name)
    print("=" * 78)

    print(
        f"backend                = "
        f"{mesh.backend.name}"
    )

    print(
        f"device                 = "
        f"{mesh.device}"
    )

    print(
        f"cell type              = "
        f"{mesh.cell_type.name}"
    )

    print(
        f"geometric dimension    = "
        f"{mesh.geometric_dimension}"
    )

    print(
        f"topological dimension  = "
        f"{mesh.topological_dimension}"
    )

    print(
        f"order                  = "
        f"{mesh.order}"
    )

    print(
        f"num nodes              = "
        f"{mesh.num_nodes}"
    )

    print(
        f"num edges              = "
        f"{mesh.number_of_edges()}"
    )

    print(
        f"num cells              = "
        f"{mesh.num_cells}"
    )

    # ============================================================
    # Points
    # ============================================================

    print("\n--- points ---")

    points = to_numpy(
        mesh,
        mesh.points,
    )

    for node_id, point in enumerate(points):
        print(
            f"{node_id}: "
            f"{point.tolist()}"
        )

    # ============================================================
    # Cells
    # ============================================================

    print("\n--- cells ---")

    cells = to_numpy(
        mesh,
        mesh.cells,
    )

    for cell_id, cell in enumerate(cells):
        print(
            f"{cell_id}: "
            f"{cell.tolist()}"
        )

    # ============================================================
    # Edges
    # ============================================================

    print("\n--- edges ---")

    edges = to_numpy(
        mesh,
        mesh.entity("edge"),
    )

    for edge_id, edge in enumerate(edges):
        print(
            f"{edge_id}: "
            f"{edge.tolist()}"
        )

    # ============================================================
    # Boundary edges
    # ============================================================

    print("\n--- boundary edges ---")

    boundary_edges = to_numpy(
        mesh,
        mesh.boundary_entities("edge"),
    )

    for boundary_id, edge in enumerate(
        boundary_edges
    ):
        print(
            f"{boundary_id}: "
            f"{edge.tolist()}"
        )

    # ============================================================
    # Cell measures
    # ============================================================

    print("\n--- cell measures ---")

    measures = to_numpy(
        mesh,
        mesh.measure("cell"),
    )

    for cell_id, measure in enumerate(measures):
        print(
            f"{cell_id}: "
            f"{float(measure)}"
        )

    # ============================================================
    # Cell barycenters
    # ============================================================

    print("\n--- cell barycenters ---")

    barycenters = to_numpy(
        mesh,
        mesh.entity_barycenter("cell"),
    )

    for cell_id, center in enumerate(
        barycenters
    ):
        print(
            f"{cell_id}: "
            f"{center.tolist()}"
        )

    # ============================================================
    # Connectivity
    # ============================================================

    print_connectivity(
        mesh,
        "cell",
        "node",
    )

    print_connectivity(
        mesh,
        "cell",
        "edge",
    )

    print_cell2edge_detail(mesh)

    print_connectivity(
        mesh,
        "edge",
        "cell",
    )

    print_connectivity(
        mesh,
        "node",
        "cell",
    )

    print_connectivity(
        mesh,
        "cell",
        "cell",
    )

    # ============================================================
    # Point data
    # ============================================================

    print("\n--- point data ---")

    if not mesh.point_data:
        print("empty")
    else:
        for field_name, values in (
            mesh.point_data.items()
        ):
            print(
                f"{field_name}: "
                f"{to_numpy(mesh, values).tolist()}"
            )

    # ============================================================
    # Cell data
    # ============================================================

    print("\n--- cell data ---")

    if not mesh.cell_data:
        print("empty")
    else:
        for field_name, values in (
            mesh.cell_data.items()
        ):
            print(
                f"{field_name}: "
                f"{to_numpy(mesh, values).tolist()}"
            )


def print_refinement_result(result) -> None:
    """
    打印加密算法产生的父子映射关系。
    """
    refined_mesh = result.mesh

    print("\n" + "=" * 78)
    print("refinement result")
    print("=" * 78)

    print(
        "parent_cell =",
        to_numpy(
            refined_mesh,
            result.parent_cell,
        ).tolist(),
    )

    print(
        "child_local_id =",
        to_numpy(
            refined_mesh,
            result.child_local_id,
        ).tolist(),
    )

    if result.old_to_new_node is not None:
        print(
            "old_to_new_node =",
            to_numpy(
                refined_mesh,
                result.old_to_new_node,
            ).tolist(),
        )

    if result.refined_cells is not None:
        print(
            "refined_cells =",
            to_numpy(
                refined_mesh,
                result.refined_cells,
            ).tolist(),
        )

    print(
        "\n--- new node parent entities ---"
    )

    if not result.new_node_parent_entity:
        print("empty")
    else:
        for record in (
            result.new_node_parent_entity
        ):
            print(record)


def main() -> None:
    # ============================================================
    # Create original mesh
    # ============================================================

    mesh = MeshFactory.triangle_rectangle(
        x_min=0.0,
        x_max=1.0,
        y_min=0.0,
        y_max=1.0,
        nx=1,
        ny=1,
        diagonal="left",
    )

    mesh.cell_data["cell_id"] = list(
        range(mesh.num_cells)
    )

    # ============================================================
    # Uniform refinement
    # ============================================================

    # result = refine(
    #     mesh,
    #     method="uniform",
    # )

    # refined = result.mesh

    # ============================================================
    # Print original mesh
    # ============================================================

    print_mesh_info(
        mesh,
        name="original triangle mesh",
    )

    # ============================================================
    # Print refinement mapping
    # ============================================================

    # print_refinement_result(
    #     result
    # )

    # # ============================================================
    # # Print refined mesh
    # # ============================================================

    # print_mesh_info(
    #     refined,
    #     name="refined triangle mesh",
    # )

    # ============================================================
    # VTK visualization
    # ============================================================

    viewer = mesh.viewer(
        show_nodes=True,
        show_edges=True,
        show_boundary=False,

        show_node_ids=True,
        show_edge_ids=True,
        show_cell_ids=True,

        node_label_color=(
            0.95,
            0.20,
            0.15,
        ),

        edge_label_color=(
            0.10,
            0.45,
            0.95,
        ),

        cell_label_color=(
            0.10,
            0.70,
            0.25,
        ),

        node_label_font_size=16,
        edge_label_font_size=14,
        cell_label_font_size=15,
    )

    viewer.show()


if __name__ == "__main__":
    main()

