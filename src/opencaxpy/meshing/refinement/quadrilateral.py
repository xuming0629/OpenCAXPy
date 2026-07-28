from __future__ import annotations

from ...mesh import QuadMesh
from .base import MeshRefiner
from .point_manager import EntityPointManager
from .result import RefinementResult
from .transfer import RefinementDataTransfer
from .utils import backend_int


class QuadUniformRefiner(MeshRefiner):
    method = "uniform"
    supported_cell_types = ("quad4",)

    def refine_once(self, mesh, context):
        manager = EntityPointManager(mesh)
        cells = mesh.backend.to_numpy(mesh.cells)
        children, parents, local_ids = [], [], []

        for cid, cell in enumerate(cells):
            v0, v1, v2, v3 = map(int, cell)
            m01 = manager.edge_point((v0, v1))
            m12 = manager.edge_point((v1, v2))
            m23 = manager.edge_point((v2, v3))
            m30 = manager.edge_point((v3, v0))
            center = manager.cell_point(cid)
            local = (
                (v0, m01, center, m30),
                (m01, v1, m12, center),
                (center, m12, v2, m23),
                (m30, center, m23, v3),
            )
            children.extend(local)
            parents.extend([cid] * 4)
            local_ids.extend(range(4))

        target = QuadMesh(
            manager.build_points(),
            backend_int(mesh, children),
            backend=mesh.backend,
            device=mesh.device,
        )
        result = RefinementResult(
            target,
            backend_int(mesh, parents),
            backend_int(mesh, local_ids),
            old_to_new_node=backend_int(mesh, range(mesh.num_nodes)),
            new_node_parent_entity=tuple(manager.records),
            refined_cells=backend_int(mesh, range(mesh.num_cells)),
        )
        RefinementDataTransfer().transfer(mesh, result, context)
        return result
