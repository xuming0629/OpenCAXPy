from __future__ import annotations

from ...mesh import TetraMesh
from .base import MeshRefiner
from .point_manager import EntityPointManager
from .result import RefinementResult
from .transfer import RefinementDataTransfer
from .utils import backend_int


class TetraUniformRefiner(MeshRefiner):
    """Red refinement: one Tetra4 becomes eight Tetra4 cells."""

    method = "uniform"
    supported_cell_types = ("tetra4",)

    def refine_once(self, mesh, context):
        manager = EntityPointManager(mesh)
        cells = mesh.backend.to_numpy(mesh.cells)
        children, parents, local_ids = [], [], []

        for cid, cell in enumerate(cells):
            a, b, c, d = map(int, cell)
            ab = manager.edge_point((a,b))
            ac = manager.edge_point((a,c))
            ad = manager.edge_point((a,d))
            bc = manager.edge_point((b,c))
            bd = manager.edge_point((b,d))
            cd = manager.edge_point((c,d))

            # Four corner tetrahedra and four tetrahedra splitting
            # the central octahedron along diagonal ab-cd.
            local = (
                (a, ab, ac, ad),
                (ab, b, bc, bd),
                (ac, bc, c, cd),
                (ad, bd, cd, d),
                (ab, ac, ad, cd),
                (ab, ac, bc, cd),
                (ab, ad, bd, cd),
                (ab, bc, bd, cd),
            )
            children.extend(local)
            parents.extend([cid] * 8)
            local_ids.extend(range(8))

        target = TetraMesh(
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
