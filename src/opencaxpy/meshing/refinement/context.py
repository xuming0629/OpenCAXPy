from __future__ import annotations

from dataclasses import dataclass, field
from numbers import Integral
from typing import Any


@dataclass(slots=True)
class RefinementContext:
    method: str
    marked_cells: Any | None = None
    levels: int = 1
    conforming: bool = True
    preserve_boundary: bool = True
    transfer_point_data: bool = True
    transfer_cell_data: bool = True
    options: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.levels, Integral):
            raise TypeError("levels must be an integer")

        self.levels = int(self.levels)

        if self.levels < 0:
            raise ValueError("levels must be non-negative")
