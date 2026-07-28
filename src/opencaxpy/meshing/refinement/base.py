from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from .context import RefinementContext
from .result import RefinementResult
from .utils import backend_int


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

    def refine(self, mesh, context: RefinementContext) -> RefinementResult:
        """Refine ``mesh`` for ``context.levels`` successive levels.

        ``parent_cell`` in the returned result describes the last refinement
        step, while ``parent_cell_original`` maps every final cell back to the
        original input mesh.
        """
        self.validate(mesh, context)

        if context.levels == 0:
            return self._identity_result(mesh)

        current_mesh = mesh
        original_parent_np = np.arange(mesh.num_cells, dtype=np.int64)
        level_results: list[RefinementResult] = []

        for level in range(context.levels):
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

            result = self.refine_once(current_mesh, one_level)

            parent_previous_np = current_mesh.backend.to_numpy(
                result.parent_cell
            ).astype(np.int64, copy=False)

            # Compose final-cell -> previous-level-cell with
            # previous-level-cell -> original-cell.
            original_parent_np = original_parent_np[parent_previous_np]
            result.parent_cell_original = backend_int(
                result.mesh,
                original_parent_np,
            )
            result.levels = level + 1
            result.metadata = dict(result.metadata)
            result.metadata.update(
                {
                    "level": level + 1,
                    "levels_requested": context.levels,
                }
            )

            level_results.append(result)
            current_mesh = result.mesh

        final_result = level_results[-1]
        final_result.parent_cell_original = backend_int(
            final_result.mesh,
            original_parent_np,
        )
        final_result.levels = context.levels
        final_result.level_results = tuple(level_results)
        final_result.metadata = dict(final_result.metadata)
        final_result.metadata.update(
            {
                "levels": context.levels,
                "original_num_cells": mesh.num_cells,
                "final_num_cells": final_result.mesh.num_cells,
            }
        )
        return final_result

    @staticmethod
    def _identity_result(mesh) -> RefinementResult:
        """Return a level-zero result without changing or copying the mesh."""
        cell_ids = mesh.backend.arange(
            mesh.num_cells,
            dtype=mesh.backend.dtype_int(),
            device=mesh.device,
        )
        node_ids = mesh.backend.arange(
            mesh.num_nodes,
            dtype=mesh.backend.dtype_int(),
            device=mesh.device,
        )
        child_ids = mesh.backend.zeros(
            (mesh.num_cells,),
            dtype=mesh.backend.dtype_int(),
            device=mesh.device,
        )

        return RefinementResult(
            mesh=mesh,
            parent_cell=cell_ids,
            child_local_id=child_ids,
            old_to_new_node=node_ids,
            new_node_parent_entity=(),
            refined_cells=mesh.backend.zeros(
                (0,),
                dtype=mesh.backend.dtype_int(),
                device=mesh.device,
            ),
            parent_cell_original=cell_ids,
            levels=0,
            level_results=(),
            metadata={
                "levels": 0,
                "original_num_cells": mesh.num_cells,
                "final_num_cells": mesh.num_cells,
            },
        )

    @abstractmethod
    def refine_once(self, mesh, context: RefinementContext):
        raise NotImplementedError
