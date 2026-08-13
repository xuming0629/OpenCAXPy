from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class DemoMesh:
    """Minimal mesh object used only by visualization examples.

    It intentionally mirrors the mesh attributes consumed by Visualization v2.0,
    so the examples can be run before a solver/problem layer is involved.
    """

    points: np.ndarray
    cells: np.ndarray
    cell_type: str
    geometric_dimension: int
    topological_dimension: int

    def entity_barycenter(self, entity_type: str) -> np.ndarray:
        if entity_type == "cell":
            return self.points[self.cells].mean(axis=1)
        if entity_type == "edge":
            edges = self._edges()
            return self.points[edges].mean(axis=1)
        if entity_type == "face" and self.topological_dimension == 3:
            faces = self._tetra_faces()
            return self.points[faces].mean(axis=1)
        raise ValueError(f"Unsupported entity type: {entity_type!r}")

    def _edges(self) -> np.ndarray:
        if self.cell_type == "triangle3":
            local_edges = ((0, 1), (1, 2), (2, 0))
        elif self.cell_type == "quad4":
            local_edges = ((0, 1), (1, 2), (2, 3), (3, 0))
        elif self.cell_type == "tetra4":
            local_edges = ((0, 1), (1, 2), (2, 0), (0, 3), (1, 3), (2, 3))
        else:
            raise NotImplementedError(self.cell_type)

        edges = {
            tuple(sorted((int(cell[a]), int(cell[b]))))
            for cell in self.cells
            for a, b in local_edges
        }
        return np.asarray(sorted(edges), dtype=int)

    def _tetra_faces(self) -> np.ndarray:
        if self.cell_type != "tetra4":
            raise NotImplementedError(self.cell_type)
        local_faces = ((0, 1, 2), (0, 1, 3), (1, 2, 3), (0, 2, 3))
        faces = {
            tuple(sorted(int(cell[i]) for i in face))
            for cell in self.cells
            for face in local_faces
        }
        return np.asarray(sorted(faces), dtype=int)


def triangle_mesh() -> DemoMesh:
    points = np.array(
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [1.0, 1.0],
            [0.0, 1.0],
            [0.5, 0.5],
        ],
        dtype=float,
    )
    cells = np.array(
        [
            [0, 1, 4],
            [1, 2, 4],
            [2, 3, 4],
            [3, 0, 4],
        ],
        dtype=int,
    )
    return DemoMesh(points, cells, "triangle3", 2, 2)


def coarse_triangle_mesh() -> DemoMesh:
    points = np.array(
        [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]], dtype=float
    )
    cells = np.array([[0, 1, 2], [0, 2, 3]], dtype=int)
    return DemoMesh(points, cells, "triangle3", 2, 2)


def tetra_mesh() -> DemoMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ],
        dtype=float,
    )
    cells = np.array([[0, 1, 2, 3]], dtype=int)
    return DemoMesh(points, cells, "tetra4", 3, 3)
