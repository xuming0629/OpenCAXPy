from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CellType:
    name: str
    dimension: int
    num_nodes: int
    local_edges: tuple[tuple[int, ...], ...]
    local_faces: tuple[tuple[int, ...], ...] = ()

CELL_TYPES = {
    "line2": CellType("line2", 1, 2, ((0, 1),)),
    "triangle3": CellType(
        "triangle3", 2, 3,
        ((1, 2), (2, 0), (0, 1)),
    ),
    "quad4": CellType(
        "quad4", 2, 4,
        ((0, 1), (1, 2), (2, 3), (3, 0)),
    ),
    "tetra4": CellType(
        "tetra4", 3, 4,
        (
            (0, 1), (1, 2), (2, 0),
            (0, 3), (1, 3), (2, 3),
        ),
        (
            (1, 2, 3),
            (0, 3, 2),
            (0, 1, 3),
            (0, 2, 1),
        ),
    ),
    "hexa8": CellType(
        "hexa8", 3, 8,
        (
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7),
        ),
        (
            (0, 3, 2, 1),
            (4, 5, 6, 7),
            (0, 1, 5, 4),
            (1, 2, 6, 5),
            (2, 3, 7, 6),
            (3, 0, 4, 7),
        ),
    ),
}

def get_cell_type(name: str) -> CellType:
    try:
        return CELL_TYPES[name.lower()]
    except KeyError as exc:
        raise KeyError(
            f"Unknown cell type {name!r}; "
            f"available={sorted(CELL_TYPES)}"
        ) from exc
