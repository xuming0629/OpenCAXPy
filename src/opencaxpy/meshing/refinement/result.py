from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RefinementResult:
    """Result returned by a mesh-refinement operation.

    Parameters
    ----------
    mesh
        The final refined mesh.
    parent_cell
        Parent cell IDs in the immediately previous mesh level.  This keeps
        the historical one-level API semantics.
    child_local_id
        Local child number inside the immediately previous parent cell.
    parent_cell_original
        Parent cell IDs in the original mesh passed to ``refine``.  For a
        one-level refinement this is identical to ``parent_cell``.
    levels
        Number of refinement levels that were actually applied.
    level_results
        Per-level results, ordered from the first to the last level.
    """

    mesh: Any
    parent_cell: Any
    child_local_id: Any
    old_to_new_node: Any | None = None
    new_node_parent_entity: tuple[dict[str, Any], ...] = ()
    refined_cells: Any | None = None
    refinement_level: Any | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    parent_cell_original: Any | None = None
    levels: int = 1
    level_results: tuple[Any, ...] = ()

    @property
    def parent_cell_previous_level(self):
        """Alias that makes the meaning of ``parent_cell`` explicit."""
        return self.parent_cell
