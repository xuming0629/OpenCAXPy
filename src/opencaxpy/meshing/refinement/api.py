from __future__ import annotations

from .context import RefinementContext
from .registry import refinement_registry


def refine(
    mesh,
    method: str = "uniform",
    *,
    levels: int = 1,
    **kwargs,
):
    """Refine a mesh one or more times.

    Parameters
    ----------
    mesh
        Input mesh.
    method
        Registered refinement method, such as ``"uniform"``.
    levels
        Number of successive refinement levels. ``levels=0`` returns an
        identity result whose ``mesh`` is the original mesh.
    **kwargs
        Additional :class:`RefinementContext` options, for example
        ``marked_cells`` and ``conforming``.

    Returns
    -------
    RefinementResult
        ``parent_cell`` maps final cells to the immediately previous level;
        ``parent_cell_original`` maps final cells to the original input mesh.
    """
    context = RefinementContext(
        method=method,
        levels=levels,
        **kwargs,
    )
    refiner = refinement_registry.get(mesh.cell_type.name, method)
    return refiner.refine(mesh, context)


def available_refinement_methods(mesh_or_cell_type) -> tuple[str, ...]:
    cell_type = (
        mesh_or_cell_type.cell_type.name
        if hasattr(mesh_or_cell_type, "cell_type")
        else str(mesh_or_cell_type)
    )
    return refinement_registry.methods(cell_type)
