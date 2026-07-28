from __future__ import annotations

from abc import ABC, abstractmethod

from .context import RefinementContext


class MeshRefiner(ABC):
    method: str
    supported_cell_types: tuple[str, ...]

    def supports(self, mesh) -> bool:
        return mesh.cell_type.name in self.supported_cell_types

    def validate(self, mesh, context: RefinementContext) -> None:
        if not self.supports(mesh):
            raise ValueError(
                f"{type(self).__name__} does not support {mesh.cell_type.name}"
            )

    def refine(self, mesh, context: RefinementContext):
        self.validate(mesh, context)
        current = mesh
        result = None
        for _ in range(context.levels):
            one_level = RefinementContext(
                method=context.method,
                marked_cells=context.marked_cells,
                levels=1,
                conforming=context.conforming,
                preserve_boundary=context.preserve_boundary,
                transfer_point_data=context.transfer_point_data,
                transfer_cell_data=context.transfer_cell_data,
                options=dict(context.options),
            )
            result = self.refine_once(current, one_level)
            current = result.mesh
        return result

    @abstractmethod
    def refine_once(self, mesh, context: RefinementContext):
        raise NotImplementedError
