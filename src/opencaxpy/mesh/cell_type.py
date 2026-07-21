from __future__ import annotations

from enum import Enum


class CellType(str, Enum):
    LINE2 = "line2"
    LINE3 = "line3"
    TRIANGLE3 = "triangle3"
    TRIANGLE6 = "triangle6"
    QUAD4 = "quad4"
    QUAD8 = "quad8"
    QUAD9 = "quad9"
    TETRA4 = "tetra4"
    TETRA10 = "tetra10"
    HEXA8 = "hexa8"
    HEXA20 = "hexa20"
    HEXA27 = "hexa27"

    @property
    def dimension(self) -> int:
        return CELL_INFO[self]["dimension"]

    @property
    def order(self) -> int:
        return CELL_INFO[self]["order"]

    @property
    def num_nodes(self) -> int:
        return CELL_INFO[self]["num_nodes"]

    @property
    def corner_nodes(self) -> tuple[int, ...]:
        return CELL_INFO[self]["corner_nodes"]


CELL_INFO = {
    CellType.LINE2: dict(dimension=1, order=1, num_nodes=2, corner_nodes=(0, 1)),
    CellType.LINE3: dict(dimension=1, order=2, num_nodes=3, corner_nodes=(0, 1)),
    CellType.TRIANGLE3: dict(dimension=2, order=1, num_nodes=3, corner_nodes=(0, 1, 2)),
    CellType.TRIANGLE6: dict(dimension=2, order=2, num_nodes=6, corner_nodes=(0, 1, 2)),
    CellType.QUAD4: dict(dimension=2, order=1, num_nodes=4, corner_nodes=(0, 1, 2, 3)),
    CellType.QUAD8: dict(dimension=2, order=2, num_nodes=8, corner_nodes=(0, 1, 2, 3)),
    CellType.QUAD9: dict(dimension=2, order=2, num_nodes=9, corner_nodes=(0, 1, 2, 3)),
    CellType.TETRA4: dict(dimension=3, order=1, num_nodes=4, corner_nodes=(0, 1, 2, 3)),
    CellType.TETRA10: dict(dimension=3, order=2, num_nodes=10, corner_nodes=(0, 1, 2, 3)),
    CellType.HEXA8: dict(dimension=3, order=1, num_nodes=8, corner_nodes=tuple(range(8))),
    CellType.HEXA20: dict(dimension=3, order=2, num_nodes=20, corner_nodes=tuple(range(8))),
    CellType.HEXA27: dict(dimension=3, order=2, num_nodes=27, corner_nodes=tuple(range(8))),
}
