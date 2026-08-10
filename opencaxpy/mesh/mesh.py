from __future__ import annotations
import numpy as np
from .cell_type import get_cell_type
from .topology import MeshTopology

class Mesh:
    def __init__(self, points, cells, cell_type):
        self.points = np.asarray(points, dtype=float)
        self.cells = np.asarray(cells, dtype=int)
        self.cell_type = cell_type.lower()

        desc = get_cell_type(self.cell_type)

        if self.points.ndim != 2:
            raise ValueError("points must be (NN, GD)")

        if (
            self.cells.ndim != 2
            or self.cells.shape[1] != desc.num_nodes
        ):
            raise ValueError(
                f"{self.cell_type} expects "
                f"{desc.num_nodes} nodes/cell"
            )

        if self.cells.size:
            if self.cells.min() < 0:
                raise ValueError("negative node index")
            if self.cells.max() >= len(self.points):
                raise ValueError("invalid node index")

        self._topology = None

    @property
    def descriptor(self):
        return get_cell_type(self.cell_type)

    @property
    def topology(self):
        if self._topology is None:
            self._topology = MeshTopology(
                self.cells,
                self.cell_type,
            )
        return self._topology

    @property
    def geometric_dimension(self):
        return self.points.shape[1]

    @property
    def topological_dimension(self):
        return self.descriptor.dimension

    def number_of_nodes(self):
        return len(self.points)

    def number_of_edges(self):
        return len(self.topology.edges)

    def number_of_faces(self):
        if self.topological_dimension == 2:
            return self.number_of_cells()
        return len(self.topology.faces)

    def number_of_cells(self):
        return len(self.cells)

    def entity(self, entity_type):
        if isinstance(entity_type, int):
            mapping = {
                0: "node",
                1: "edge",
                2: (
                    "cell"
                    if self.topological_dimension == 2
                    else "face"
                ),
                3: "cell",
            }
            entity_type = mapping[entity_type]

        entity_type = str(entity_type).lower()

        if entity_type in ("node", "point", "vertex"):
            return self.points
        if entity_type == "edge":
            return self.topology.edges
        if entity_type == "face":
            if self.topological_dimension == 2:
                return self.cells
            return self.topology.faces
        if entity_type == "cell":
            return self.cells

        raise ValueError(entity_type)

    def cell_coordinates(self, i):
        return self.points[self.cells[i]]

    def cell_to_edge(self):
        return self.topology.cell_to_edge()

    def cell_to_face(self):
        if self.topological_dimension == 2:
            return np.arange(
                self.number_of_cells(),
                dtype=int,
            )[:, None]
        return self.topology.cell_to_face()

    def edge_to_cell(self):
        return self.topology.edge_to_cell()

    def face_to_cell(self):
        if self.topological_dimension == 2:
            return tuple(
                (i,)
                for i in range(self.number_of_cells())
            )
        return self.topology.face_to_cell()

    def boundary_edge_index(self):
        return self.topology.boundary_edge_index()

    def boundary_face_index(self):
        if self.topological_dimension == 2:
            return np.arange(
                self.number_of_cells(),
                dtype=int,
            )
        return self.topology.boundary_face_index()

    def boundary_node_index(self):
        if self.topological_dimension == 1:
            degree = np.zeros(
                self.number_of_nodes(),
                dtype=int,
            )
            for cell in self.cells:
                degree[cell] += 1
            return np.where(degree == 1)[0]

        if self.topological_dimension == 2:
            ids = self.boundary_edge_index()
            if not len(ids):
                return np.empty(0, dtype=int)
            return np.unique(
                self.entity("edge")[ids]
            )

        ids = self.boundary_face_index()
        if not len(ids):
            return np.empty(0, dtype=int)
        return np.unique(
            self.entity("face")[ids]
        )

    def entity_barycenter(self, entity_type="cell"):
        if entity_type in ("node", "point", "vertex", 0):
            return self.points.copy()

        entity = self.entity(entity_type)
        return self.points[entity].mean(axis=1)

    def edge_length(self):
        edge = self.entity("edge")
        p = self.points[edge]
        return np.linalg.norm(
            p[:, 1] - p[:, 0],
            axis=1,
        )

    def _triangle_area(self, tri):
        a = tri[:, 1] - tri[:, 0]
        b = tri[:, 2] - tri[:, 0]

        if tri.shape[-1] == 2:
            return 0.5 * np.abs(
                a[:, 0] * b[:, 1]
                - a[:, 1] * b[:, 0]
            )

        return 0.5 * np.linalg.norm(
            np.cross(a, b),
            axis=1,
        )

    def _tetra_volume(self, tet):
        a = tet[:, 1] - tet[:, 0]
        b = tet[:, 2] - tet[:, 0]
        c = tet[:, 3] - tet[:, 0]

        return np.abs(
            np.einsum(
                "ij,ij->i",
                np.cross(a, b),
                c,
            )
        ) / 6.0

    def entity_measure(self, entity_type="cell"):
        if entity_type == "edge":
            return self.edge_length()

        if entity_type != "cell":
            raise NotImplementedError(entity_type)

        x = self.points[self.cells]

        if self.cell_type == "line2":
            return np.linalg.norm(
                x[:, 1] - x[:, 0],
                axis=1,
            )

        if self.cell_type == "triangle3":
            return self._triangle_area(x)

        if self.cell_type == "quad4":
            return (
                self._triangle_area(x[:, [0, 1, 2]])
                + self._triangle_area(x[:, [0, 2, 3]])
            )

        if self.cell_type == "tetra4":
            return self._tetra_volume(x)

        if self.cell_type == "hexa8":
            tet_ids = (
                (0, 1, 3, 4),
                (1, 2, 3, 6),
                (1, 3, 4, 6),
                (1, 4, 5, 6),
                (3, 4, 6, 7),
            )
            volume = np.zeros(
                self.number_of_cells(),
                dtype=float,
            )
            for ids in tet_ids:
                volume += self._tetra_volume(
                    x[:, ids]
                )
            return volume

        raise NotImplementedError(self.cell_type)

    def cell_quality(self):
        x = self.points[self.cells]

        if self.cell_type == "line2":
            return np.ones(self.number_of_cells())

        if self.cell_type == "triangle3":
            e2 = (
                np.sum((x[:,1]-x[:,0])**2, axis=1)
                + np.sum((x[:,2]-x[:,1])**2, axis=1)
                + np.sum((x[:,0]-x[:,2])**2, axis=1)
            )
            A = self.entity_measure("cell")
            with np.errstate(divide="ignore", invalid="ignore"):
                q = 4*np.sqrt(3)*A/e2
            return np.nan_to_num(q)

        if self.cell_type == "tetra4":
            l2 = np.zeros(self.number_of_cells())
            for a, b in self.descriptor.local_edges:
                l2 += np.sum(
                    (x[:,a]-x[:,b])**2,
                    axis=1,
                )
            V = self.entity_measure("cell")
            with np.errstate(divide="ignore", invalid="ignore"):
                q = 12*np.power(3*V, 2/3)/l2
            return np.nan_to_num(q)

        if self.cell_type in ("quad4", "hexa8"):
            lengths = self.edge_length()[
                self.cell_to_edge()
            ]
            with np.errstate(divide="ignore", invalid="ignore"):
                q = (
                    lengths.min(axis=1)
                    / lengths.max(axis=1)
                )
            return np.nan_to_num(q)

        raise NotImplementedError(self.cell_type)

    def summary(self):
        q = self.cell_quality()

        return {
            "cell_type": self.cell_type,
            "geometric_dimension": self.geometric_dimension,
            "topological_dimension": self.topological_dimension,
            "num_nodes": self.number_of_nodes(),
            "num_edges": self.number_of_edges(),
            "num_faces": self.number_of_faces(),
            "num_cells": self.number_of_cells(),
            "measure_sum": float(
                self.entity_measure("cell").sum()
            ),
            "quality_min": float(q.min())
            if len(q)
            else None,
            "quality_mean": float(q.mean())
            if len(q)
            else None,
        }
