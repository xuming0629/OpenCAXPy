from __future__ import annotations

from ...mesh import HexaMesh
from .base import MeshRefiner
from .point_manager import EntityPointManager
from .result import RefinementResult
from .transfer import RefinementDataTransfer
from .utils import backend_int


class HexaUniformRefiner(MeshRefiner):
    """One Hexa8 becomes eight Hexa8 cells."""

    method = "uniform"
    supported_cell_types = ("hexa8",)

    def refine_once(self, mesh, context):
        manager = EntityPointManager(mesh)
        cells = mesh.backend.to_numpy(mesh.cells)
        children, parents, local_ids = [], [], []

        for cid, cell in enumerate(cells):
            v = list(map(int, cell))
            # 3x3x3 logical lattice indices.
            g = {}
            corner_map = {
                (0,0,0): v[0], (2,0,0): v[1],
                (2,2,0): v[2], (0,2,0): v[3],
                (0,0,2): v[4], (2,0,2): v[5],
                (2,2,2): v[6], (0,2,2): v[7],
            }
            g.update(corner_map)

            edge_defs = {
                (1,0,0):(v[0],v[1]), (2,1,0):(v[1],v[2]),
                (1,2,0):(v[3],v[2]), (0,1,0):(v[0],v[3]),
                (1,0,2):(v[4],v[5]), (2,1,2):(v[5],v[6]),
                (1,2,2):(v[7],v[6]), (0,1,2):(v[4],v[7]),
                (0,0,1):(v[0],v[4]), (2,0,1):(v[1],v[5]),
                (2,2,1):(v[2],v[6]), (0,2,1):(v[3],v[7]),
            }
            for key, edge in edge_defs.items():
                g[key] = manager.edge_point(edge)

            face_defs = {
                (1,1,0):(v[0],v[1],v[2],v[3]),
                (1,1,2):(v[4],v[5],v[6],v[7]),
                (1,0,1):(v[0],v[1],v[5],v[4]),
                (2,1,1):(v[1],v[2],v[6],v[5]),
                (1,2,1):(v[3],v[2],v[6],v[7]),
                (0,1,1):(v[0],v[3],v[7],v[4]),
            }
            for key, face in face_defs.items():
                g[key] = manager.face_point(face)

            g[(1,1,1)] = manager.cell_point(cid)

            local_id = 0
            for k in range(2):
                for j in range(2):
                    for i in range(2):
                        child = (
                            g[(i,j,k)],
                            g[(i+1,j,k)],
                            g[(i+1,j+1,k)],
                            g[(i,j+1,k)],
                            g[(i,j,k+1)],
                            g[(i+1,j,k+1)],
                            g[(i+1,j+1,k+1)],
                            g[(i,j+1,k+1)],
                        )
                        children.append(child)
                        parents.append(cid)
                        local_ids.append(local_id)
                        local_id += 1

        target = HexaMesh(
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
