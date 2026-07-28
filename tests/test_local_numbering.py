import numpy as np

from opencaxpy import MeshFactory, TRIANGLE3, TRIANGLE6, refine


def test_triangle_descriptor_opposite_edge_numbering():
    assert TRIANGLE3.local_edges == (
        (1, 2),
        (2, 0),
        (0, 1),
    )
    assert TRIANGLE6.local_edges == (
        (1, 3, 2),
        (2, 4, 0),
        (0, 5, 1),
    )


def test_left_diagonal_right_angle_first_and_ccw():
    mesh = MeshFactory.triangle_rectangle(
        nx=1,
        ny=1,
        diagonal="left",
    )
    cells = mesh.backend.to_numpy(mesh.cells)
    assert cells.tolist() == [[0, 1, 2], [3, 2, 1]]

    points = mesh.backend.to_numpy(mesh.points)
    for cell in cells:
        p0, p1, p2 = points[cell]
        u = p1 - p0
        v = p2 - p0
        signed_twice_area = u[0] * v[1] - u[1] * v[0]
        assert signed_twice_area > 0.0
        assert abs(np.dot(p1 - p0, p2 - p0)) < 1.0e-12


def test_cell2edge_columns_follow_opposite_node_rule():
    mesh = MeshFactory.triangle_rectangle(
        nx=1,
        ny=1,
        diagonal="left",
    )
    cells = mesh.backend.to_numpy(mesh.cells)
    edges = mesh.backend.to_numpy(mesh.entity("edge"))
    cell2edge = mesh.connectivity("cell", "edge").to_lists()

    for cell_id, cell in enumerate(cells):
        for local_edge_id, (la, lb) in enumerate(TRIANGLE3.local_edges):
            global_edge_id = cell2edge[cell_id][local_edge_id]
            expected = tuple(sorted((int(cell[la]), int(cell[lb]))))
            actual = tuple(map(int, edges[global_edge_id]))
            assert actual == expected
            assert int(cell[local_edge_id]) not in actual


def test_cell_to_edge_sign_matches_local_direction():
    mesh = MeshFactory.triangle_rectangle(
        nx=1,
        ny=1,
        diagonal="left",
    )
    cells = mesh.backend.to_numpy(mesh.cells)
    edges = mesh.backend.to_numpy(mesh.entity("edge"))
    c2e = mesh.connectivity("cell", "edge").to_lists()
    signs = mesh.backend.to_numpy(mesh.cell_to_edge_sign())

    for cid, cell in enumerate(cells):
        for lid, (la, lb) in enumerate(TRIANGLE3.local_edges):
            directed = (int(cell[la]), int(cell[lb]))
            canonical = tuple(map(int, edges[c2e[cid][lid]]))
            expected = 1 if directed == canonical else -1
            assert int(signs[cid, lid]) == expected


def test_uniform_refinement_preserves_right_angle_first():
    mesh = MeshFactory.triangle_rectangle(
        nx=1,
        ny=1,
        diagonal="left",
    )
    refined = refine(mesh, method="uniform").mesh
    points = refined.backend.to_numpy(refined.points)
    cells = refined.backend.to_numpy(refined.cells)

    for cell in cells:
        p0, p1, p2 = points[cell]
        u = p1 - p0
        v = p2 - p0
        assert u[0] * v[1] - u[1] * v[0] > 0.0
        assert abs(np.dot(p1 - p0, p2 - p0)) < 1.0e-12


def test_global_edge_discovery_is_independent_of_triangle_local_edge_order():
    mesh = MeshFactory.triangle_rectangle(
        nx=1,
        ny=1,
        diagonal="left",
    )

    edges = mesh.backend.to_numpy(mesh.entity("edge"))
    assert edges.tolist() == [
        [0, 1],
        [1, 2],
        [0, 2],
        [2, 3],
        [1, 3],
    ]

    assert mesh.connectivity("cell", "edge").to_lists() == [
        [1, 2, 0],
        [1, 4, 3],
    ]

    assert mesh.connectivity("edge", "cell").to_lists() == [
        [0],
        [0, 1],
        [0],
        [1],
        [1],
    ]
