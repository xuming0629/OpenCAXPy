from __future__ import annotations

from .context import RefinementContext
from .registry import refinement_registry


def refine(mesh, method: str = "uniform", **kwargs):
    context = RefinementContext(method=method, **kwargs)
    refiner = refinement_registry.get(mesh.cell_type.name, method)
    return refiner.refine(mesh, context)


def available_refinement_methods(mesh_or_cell_type) -> tuple[str, ...]:
    cell_type = (
        mesh_or_cell_type.cell_type.name
        if hasattr(mesh_or_cell_type, "cell_type")
        else str(mesh_or_cell_type)
    )
    return refinement_registry.methods(cell_type)
