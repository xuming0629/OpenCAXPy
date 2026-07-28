from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from ..core import CellTypeError, Registry


@dataclass(frozen=True, slots=True)
class CellDescriptor:
    name: str
    topological_dimension: int
    order: int
    num_nodes: int
    corner_nodes: tuple[int, ...]
    local_edges: tuple[tuple[int, ...], ...]
    local_faces: tuple[tuple[int, ...], ...] = ()
    topology_edge_order: tuple[tuple[int, int], ...] = ()

    def __post_init__(self) -> None:
        if not self.name:
            raise CellTypeError("cell descriptor name cannot be empty")
        if self.topological_dimension < 0:
            raise CellTypeError(
                "topological_dimension must be non-negative"
            )
        if self.order <= 0:
            raise CellTypeError("order must be positive")
        if self.num_nodes <= 0:
            raise CellTypeError("num_nodes must be positive")
        if not self.corner_nodes:
            raise CellTypeError("corner_nodes cannot be empty")
        if max(self.corner_nodes) >= self.num_nodes:
            raise CellTypeError("corner node id is out of range")

        for entity in (*self.local_edges, *self.local_faces):
            if not entity:
                raise CellTypeError("local entity cannot be empty")
            if min(entity) < 0 or max(entity) >= self.num_nodes:
                raise CellTypeError(
                    f"local entity {entity} contains invalid node ids"
                )

        for edge in self.topology_edge_order:
            if len(edge) != 2:
                raise CellTypeError(
                    "topology_edge_order entries must contain two node ids"
                )
            if edge[0] == edge[1]:
                raise CellTypeError("topology discovery edge is degenerate")
            if min(edge) < 0 or max(edge) >= self.num_nodes:
                raise CellTypeError(
                    f"topology discovery edge {edge} contains invalid node ids"
                )

        if (
            self.topology_edge_order
            and len(self.topology_edge_order) != len(self.local_edges)
        ):
            raise CellTypeError(
                "topology_edge_order and local_edges must have equal length"
            )

    @property
    def family(self) -> str:
        for suffix in ("3", "4", "6", "8", "9", "10", "20", "27"):
            if self.name.endswith(suffix):
                return self.name[: -len(suffix)]
        return self.name

    @property
    def num_corner_nodes(self) -> int:
        return len(self.corner_nodes)

    def corner_connectivity(self, cells):
        return cells[:, self.corner_nodes]

    def edge_corner_nodes(self) -> tuple[tuple[int, int], ...]:
        values: list[tuple[int, int]] = []
        for edge in self.local_edges:
            values.append((edge[0], edge[-1]))
        return tuple(values)

    def edge_internal_nodes(self) -> tuple[tuple[int, ...], ...]:
        return tuple(edge[1:-1] for edge in self.local_edges)

    @property
    def edge_discovery_order(self) -> tuple[tuple[int, int], ...]:
        """Edges used only to discover and number global edge entities.

        ``local_edges`` keeps the semantic local-edge numbering used by
        ``cell2edge``.  This independent order prevents a change in local
        numbering from unexpectedly renumbering all global edges.
        """
        if self.topology_edge_order:
            return self.topology_edge_order
        return self.edge_corner_nodes()

    @property
    def num_local_nodes(self) -> int:
        return self.num_nodes

    @property
    def num_local_edges(self) -> int:
        return len(self.local_edges)

    @property
    def num_local_faces(self) -> int:
        return len(self.local_faces)

    def local_node_ids(self) -> tuple[int, ...]:
        """Return the ordered local node IDs stored in cell2node columns."""
        return tuple(range(self.num_nodes))

    def local_edge_ids(self) -> tuple[int, ...]:
        """Return the ordered local edge IDs stored in cell2edge columns."""
        return tuple(range(len(self.local_edges)))

    def local_face_ids(self) -> tuple[int, ...]:
        return tuple(range(len(self.local_faces)))

    def opposite_edge_of_node(self, local_node_id: int) -> int:
        """Return the edge opposite a local node for simplex triangles.

        OpenCAXPy uses the convention ``local edge i`` is opposite
        ``local node i`` for Triangle3/Triangle6.
        """
        if self.family != "triangle":
            raise CellTypeError(
                "opposite_edge_of_node is currently defined for triangles"
            )
        local_node_id = int(local_node_id)
        if local_node_id not in self.corner_nodes:
            raise CellTypeError(
                f"{local_node_id} is not a triangle corner-node ID"
            )
        return local_node_id


CELL_TYPES: Registry[CellDescriptor] = Registry("cell type")


def register_cell_type(
    descriptor: CellDescriptor,
    *,
    replace: bool = False,
) -> CellDescriptor:
    CELL_TYPES.register(
        descriptor.name,
        descriptor,
        replace=replace,
    )
    return descriptor


def get_cell_type(
    cell_type: str | CellDescriptor,
) -> CellDescriptor:
    if isinstance(cell_type, CellDescriptor):
        return cell_type
    return CELL_TYPES.get(cell_type)


TRIANGLE3 = register_cell_type(
    CellDescriptor(
        name="triangle3",
        topological_dimension=2,
        order=1,
        num_nodes=3,
        corner_nodes=(0, 1, 2),
        # Triangle local-numbering convention:
        #   local edge 0 is opposite local node 0
        #   local edge 1 is opposite local node 1
        #   local edge 2 is opposite local node 2
        # For a counter-clockwise cell [v0, v1, v2], every directed
        # local edge also follows the counter-clockwise boundary.
        local_edges=(
            (1, 2),
            (2, 0),
            (0, 1),
        ),
        topology_edge_order=(
            (0, 1),
            (1, 2),
            (2, 0),
        ),
    )
)

TRIANGLE6 = register_cell_type(
    CellDescriptor(
        name="triangle6",
        topological_dimension=2,
        order=2,
        num_nodes=6,
        corner_nodes=(0, 1, 2),
        # High-order nodes 3, 4 and 5 belong to the edges opposite
        # local corner nodes 0, 1 and 2 respectively.
        local_edges=(
            (1, 3, 2),
            (2, 4, 0),
            (0, 5, 1),
        ),
        topology_edge_order=(
            (0, 1),
            (1, 2),
            (2, 0),
        ),
    )
)

QUAD4 = register_cell_type(
    CellDescriptor(
        name="quad4",
        topological_dimension=2,
        order=1,
        num_nodes=4,
        corner_nodes=(0, 1, 2, 3),
        local_edges=(
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
        ),
    )
)

QUAD8 = register_cell_type(
    CellDescriptor(
        name="quad8",
        topological_dimension=2,
        order=2,
        num_nodes=8,
        corner_nodes=(0, 1, 2, 3),
        local_edges=(
            (0, 4, 1),
            (1, 5, 2),
            (2, 6, 3),
            (3, 7, 0),
        ),
    )
)

QUAD9 = register_cell_type(
    CellDescriptor(
        name="quad9",
        topological_dimension=2,
        order=2,
        num_nodes=9,
        corner_nodes=(0, 1, 2, 3),
        local_edges=(
            (0, 4, 1),
            (1, 5, 2),
            (2, 6, 3),
            (3, 7, 0),
        ),
    )
)

TETRA4 = register_cell_type(
    CellDescriptor(
        name="tetra4",
        topological_dimension=3,
        order=1,
        num_nodes=4,
        corner_nodes=(0, 1, 2, 3),
        local_edges=(
            (0, 1),
            (1, 2),
            (2, 0),
            (0, 3),
            (1, 3),
            (2, 3),
        ),
        local_faces=(
            (0, 2, 1),
            (0, 1, 3),
            (1, 2, 3),
            (2, 0, 3),
        ),
    )
)

HEXA8 = register_cell_type(
    CellDescriptor(
        name="hexa8",
        topological_dimension=3,
        order=1,
        num_nodes=8,
        corner_nodes=(0, 1, 2, 3, 4, 5, 6, 7),
        local_edges=(
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
        ),
        local_faces=(
            (0, 3, 2, 1),
            (4, 5, 6, 7),
            (0, 1, 5, 4),
            (1, 2, 6, 5),
            (2, 3, 7, 6),
            (3, 0, 4, 7),
        ),
    )
)
