from opencaxpy import TriangleMesh


def test_triangle6_base_and_high_order_topology():
    mesh = TriangleMesh(
        [
            [0, 0], [1, 0], [0, 1], [1, 1],
            [0.5, 0], [0.5, 0.5], [0, 0.5],
            [1, 0.5], [0.5, 1],
        ],
        [
            # local edge 0=(1,2)->node 5
            # local edge 1=(2,0)->node 6
            # local edge 2=(0,1)->node 4
            [0, 1, 2, 5, 6, 4],
            # local edge 0=(3,2)->node 8
            # local edge 1=(2,1)->node 5
            # local edge 2=(1,3)->node 7
            [1, 3, 2, 8, 5, 7],
        ],
        cell_type="triangle6",
    )

    assert mesh.number_of_edges() == 5
    high_order = mesh.topology.high_order_edge_nodes()

    assert high_order is not None
    assert [5] in high_order.to_lists()
