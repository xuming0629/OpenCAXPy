from __future__ import annotations
import numpy as np
from .cell_type import get_cell_type

class MeshTopology:
    def __init__(self, cells, cell_type):
        self.cells = np.asarray(cells, dtype=int)
        self.cell_type = cell_type
        self.descriptor = get_cell_type(cell_type)

        self.edges, self._cell_to_edge = self._build(
            self.descriptor.local_edges
        )

        if self.descriptor.dimension == 3:
            self.faces, self._cell_to_face = self._build(
                self.descriptor.local_faces
            )
        else:
            self.faces = np.empty((0, 0), dtype=int)
            self._cell_to_face = np.empty(
                (len(self.cells), 0),
                dtype=int,
            )

        self._edge_to_cell = self._reverse(
            self._cell_to_edge
        )
        self._face_to_cell = self._reverse(
            self._cell_to_face
        )

    def _build(self, local_entities):
        if not local_entities:
            return (
                np.empty((0, 0), dtype=int),
                np.empty((len(self.cells), 0), dtype=int),
            )

        table = {}
        entities = []
        c2e = np.empty(
            (len(self.cells), len(local_entities)),
            dtype=int,
        )

        for ci, cell in enumerate(self.cells):
            for li, local in enumerate(local_entities):
                key = tuple(
                    sorted(int(cell[j]) for j in local)
                )
                idx = table.get(key)

                if idx is None:
                    idx = len(entities)
                    table[key] = idx
                    entities.append(key)

                c2e[ci, li] = idx

        return np.asarray(entities, dtype=int), c2e

    def _reverse(self, c2e):
        if not c2e.size:
            return tuple()

        result = [
            []
            for _ in range(int(c2e.max()) + 1)
        ]

        for ci, row in enumerate(c2e):
            for entity_id in row:
                result[int(entity_id)].append(ci)

        return tuple(
            tuple(items)
            for items in result
        )

    def cell_to_edge(self):
        return self._cell_to_edge.copy()

    def cell_to_face(self):
        return self._cell_to_face.copy()

    def edge_to_cell(self):
        return self._edge_to_cell

    def face_to_cell(self):
        return self._face_to_cell

    def boundary_edge_index(self):
        if self.descriptor.dimension == 1:
            return np.arange(
                len(self.edges),
                dtype=int,
            )

        if self.descriptor.dimension == 2:
            return np.asarray(
                [
                    i
                    for i, adj in enumerate(self._edge_to_cell)
                    if len(adj) == 1
                ],
                dtype=int,
            )

        boundary_faces = self.faces[
            self.boundary_face_index()
        ]
        boundary_sets = [
            set(map(int, f))
            for f in boundary_faces
        ]

        ids = []

        for i, edge in enumerate(self.edges):
            nodes = set(map(int, edge))
            if any(
                nodes.issubset(face)
                for face in boundary_sets
            ):
                ids.append(i)

        return np.asarray(ids, dtype=int)

    def boundary_face_index(self):
        if self.descriptor.dimension != 3:
            return np.empty(0, dtype=int)

        return np.asarray(
            [
                i
                for i, adj in enumerate(self._face_to_cell)
                if len(adj) == 1
            ],
            dtype=int,
        )
