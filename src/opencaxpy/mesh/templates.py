from __future__ import annotations

from .cell_type import CellType

LOCAL_EDGES = {
    CellType.LINE2: ((0, 1),),
    CellType.LINE3: ((0, 1),),
    CellType.TRIANGLE3: ((0, 1), (1, 2), (2, 0)),
    CellType.TRIANGLE6: ((0, 1), (1, 2), (2, 0)),
    CellType.QUAD4: ((0, 1), (1, 2), (2, 3), (3, 0)),
    CellType.QUAD8: ((0, 1), (1, 2), (2, 3), (3, 0)),
    CellType.QUAD9: ((0, 1), (1, 2), (2, 3), (3, 0)),
    CellType.TETRA4: (
        (0, 1), (1, 2), (2, 0),
        (0, 3), (1, 3), (2, 3),
    ),
    CellType.TETRA10: (
        (0, 1), (1, 2), (2, 0),
        (0, 3), (1, 3), (2, 3),
    ),
    CellType.HEXA8: (
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    ),
}

LOCAL_FACES = {
    CellType.TETRA4: (
        (0, 2, 1),
        (0, 1, 3),
        (1, 2, 3),
        (2, 0, 3),
    ),
    CellType.TETRA10: (
        (0, 2, 1),
        (0, 1, 3),
        (1, 2, 3),
        (2, 0, 3),
    ),
    CellType.HEXA8: (
        (0, 3, 2, 1),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ),
}
