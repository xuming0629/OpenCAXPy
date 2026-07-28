from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RefinementResult:
    mesh: Any
    parent_cell: Any
    child_local_id: Any
    old_to_new_node: Any | None = None
    new_node_parent_entity: tuple[dict[str, Any], ...] = ()
    refined_cells: Any | None = None
    refinement_level: Any | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
