from __future__ import annotations

import numpy as np

from ...mesh import TriangleMesh
from .base import MeshRefiner
from .point_manager import EntityPointManager
from .result import RefinementResult
from .transfer import RefinementDataTransfer
from .utils import backend_int, marked_cell_ids


def _edge_key(a, b):
    a, b = int(a), int(b)
    return (a, b) if a < b else (b, a)


class TriangleUniformRefiner(MeshRefiner):
    method = "uniform"
    supported_cell_types = ("triangle3",)

    def refine_once(self, mesh, context):
        manager = EntityPointManager(mesh)
        cells = mesh.backend.to_numpy(mesh.cells)
        children, parents, local_ids = [], [], []

        for cid, (a, b, c) in enumerate(cells):
            a, b, c = map(int, (a, b, c))
            ab = manager.edge_point((a, b))
            bc = manager.edge_point((b, c))
            ca = manager.edge_point((c, a))
            # Parent convention:
            #   local node 0 is the right-angle vertex when the parent
            #   comes from TriangleRectangleGenerator, and nodes are CCW.
            # Every child below preserves the same convention.
            local = (
                (a, ab, ca),
                (ab, b, bc),
                (ca, bc, c),
                (bc, ca, ab),
            )
            children.extend(local)
            parents.extend([cid] * 4)
            local_ids.extend(range(4))

        target = TriangleMesh(
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


class _TriangleBisectionRefiner(MeshRefiner):
    strategy: str

    def _selected_edge(self, mesh, points, cell):
        local_edges = mesh.cell_type.edge_corner_nodes()
        edges = [
            _edge_key(cell[local_a], cell[local_b])
            for local_a, local_b in local_edges
        ]
        if self.strategy == "newest_vertex":
            # Triangle convention: local edge 0 is opposite local node 0.
            return edges[0]
        lengths = [
            np.linalg.norm(points[v] - points[u])
            for u, v in edges
        ]
        return edges[int(np.argmax(lengths))]

    def refine_once(self, mesh, context):
        points = mesh.backend.to_numpy(mesh.points)
        cells = mesh.backend.to_numpy(mesh.cells)
        marked = marked_cell_ids(mesh, context.marked_cells)
        edge_to_cells = {}
        local_edges = mesh.cell_type.edge_corner_nodes()
        for cid, cell in enumerate(cells):
            for local_a, local_b in local_edges:
                edge = _edge_key(cell[local_a], cell[local_b])
                edge_to_cells.setdefault(edge, []).append(cid)

        split_edge_by_cell = {
            cid: self._selected_edge(mesh, points, cells[cid]) for cid in marked
        }

        if context.conforming:
            # Split every neighboring cell sharing a chosen edge.
            changed = True
            while changed:
                changed = False
                for edge in tuple(split_edge_by_cell.values()):
                    for cid in edge_to_cells.get(edge, []):
                        if cid not in split_edge_by_cell:
                            split_edge_by_cell[cid] = edge
                            changed = True

        manager = EntityPointManager(mesh)
        children, parents, local_ids = [], [], []

        for cid, cell in enumerate(cells):
            a, b, c = map(int, cell)
            if cid not in split_edge_by_cell:
                children.append((a, b, c))
                parents.append(cid)
                local_ids.append(0)
                continue

            edge = split_edge_by_cell[cid]
            m = manager.edge_point(edge)
            u, v = edge
            w = ({a, b, c} - {u, v}).pop()
            children.extend(((u, m, w), (m, v, w)))
            parents.extend((cid, cid))
            local_ids.extend((0, 1))

        target = TriangleMesh(
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
            refined_cells=backend_int(mesh, sorted(split_edge_by_cell)),
        )
        RefinementDataTransfer().transfer(mesh, result, context)
        return result


class TriangleLongestEdgeRefiner(_TriangleBisectionRefiner):
    method = "longest_edge"
    strategy = "longest_edge"
    supported_cell_types = ("triangle3",)


class TriangleNewestVertexRefiner(_TriangleBisectionRefiner):
    method = "newest_vertex"
    strategy = "newest_vertex"
    supported_cell_types = ("triangle3",)
