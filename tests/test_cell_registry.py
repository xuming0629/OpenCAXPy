from opencaxpy import (
    CELL_TYPES,
    CellDescriptor,
    get_cell_type,
    register_cell_type,
)


def test_builtin_cell_descriptors():
    triangle6 = get_cell_type("triangle6")

    assert triangle6.order == 2
    assert triangle6.corner_nodes == (0, 1, 2)
    assert triangle6.edge_internal_nodes() == (
        (3,),
        (4,),
        (5,),
    )


def test_custom_cell_registration():
    descriptor = CellDescriptor(
        name="line2_test",
        topological_dimension=1,
        order=1,
        num_nodes=2,
        corner_nodes=(0, 1),
        local_edges=((0, 1),),
    )

    register_cell_type(descriptor, replace=True)

    assert CELL_TYPES.get("line2_test") is descriptor
