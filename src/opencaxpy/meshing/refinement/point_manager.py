from __future__ import annotations

import numpy as np


class EntityPointManager:
    """Creates and deduplicates points attached to mesh entities."""

    def __init__(self, mesh) -> None:
        self.mesh = mesh
        self.backend = mesh.backend
        self.original_point_count = mesh.num_nodes
        self.points = self.backend.to_numpy(mesh.points).tolist()

        self._edge_points = {}
        self._face_points = {}
        self._cell_points = {}
        self.records = []

    def _append(self, coordinates, entity_type, entity_key):
        node_id = len(self.points)
        self.points.append(np.asarray(coordinates, dtype=float).tolist())
        self.records.append({
            "node_id": node_id,
            "parent_entity_type": entity_type,
            "parent_entity": tuple(int(v) for v in entity_key),
        })
        return node_id

    def edge_point(self, node_ids) -> int:
        key = tuple(sorted(int(v) for v in node_ids))
        if key not in self._edge_points:
            coords = self.mesh.backend.to_numpy(
                self.mesh.points[list(key)]
            ).mean(axis=0)
            self._edge_points[key] = self._append(coords, "edge", key)
        return self._edge_points[key]

    def face_point(self, node_ids) -> int:
        key = tuple(sorted(int(v) for v in node_ids))
        if key not in self._face_points:
            coords = self.mesh.backend.to_numpy(
                self.mesh.points[list(key)]
            ).mean(axis=0)
            self._face_points[key] = self._append(coords, "face", key)
        return self._face_points[key]

    def cell_point(self, cell_id: int) -> int:
        cell_id = int(cell_id)
        if cell_id not in self._cell_points:
            cell = self.mesh.backend.to_numpy(self.mesh.cells[cell_id])
            coords = self.mesh.backend.to_numpy(
                self.mesh.points[cell]
            ).mean(axis=0)
            self._cell_points[cell_id] = self._append(
                coords, "cell", (cell_id,)
            )
        return self._cell_points[cell_id]

    def build_points(self):
        return self.backend.asarray(
            self.points,
            dtype=self.backend.dtype_float(),
            device=self.mesh.device,
        )
