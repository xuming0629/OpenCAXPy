from __future__ import annotations

from typing import Any

from ..core import ArrayBackend
from .cell_type import CellDescriptor, get_cell_type
from .mesh import Mesh


class _FamilyMesh(Mesh):
    family: str

    def __init__(
        self,
        points: Any,
        cells: Any,
        cell_type: str | CellDescriptor,
        *,
        backend: str | ArrayBackend | None = None,
        device=None,
    ) -> None:
        descriptor = get_cell_type(cell_type)
        if descriptor.family != self.family:
            raise ValueError(
                f"{type(self).__name__} requires cell family {self.family!r}, "
                f"got {descriptor.family!r}"
            )
        super().__init__(
            points,
            cells,
            descriptor,
            backend=backend,
            device=device,
        )


class TriangleMesh(_FamilyMesh):
    family = "triangle"

    def __init__(
        self,
        points: Any,
        cells: Any,
        cell_type: str | CellDescriptor = "triangle3",
        **kwargs,
    ) -> None:
        super().__init__(points, cells, cell_type, **kwargs)


class QuadMesh(_FamilyMesh):
    family = "quad"

    def __init__(
        self,
        points: Any,
        cells: Any,
        cell_type: str | CellDescriptor = "quad4",
        **kwargs,
    ) -> None:
        super().__init__(points, cells, cell_type, **kwargs)


class TetraMesh(_FamilyMesh):
    family = "tetra"

    def __init__(
        self,
        points: Any,
        cells: Any,
        cell_type: str | CellDescriptor = "tetra4",
        **kwargs,
    ) -> None:
        super().__init__(points, cells, cell_type, **kwargs)


class HexaMesh(_FamilyMesh):
    family = "hexa"

    def __init__(
        self,
        points: Any,
        cells: Any,
        cell_type: str | CellDescriptor = "hexa8",
        **kwargs,
    ) -> None:
        super().__init__(points, cells, cell_type, **kwargs)
