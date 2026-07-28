from __future__ import annotations

from typing import Any

from ..core import ArrayBackend, get_backend
from .cell_type import CellDescriptor, get_cell_type
from .data import MeshData
from .geometry import MeshGeometry
from .topology import Topology


class Mesh:
    """Backend-neutral mesh data container for CAX applications."""

    def __init__(
        self,
        points: Any,
        cells: Any,
        cell_type: str | CellDescriptor,
        *,
        backend: str | ArrayBackend | None = None,
        device=None,
    ) -> None:
        self.backend = get_backend(backend)
        self.cell_type = get_cell_type(cell_type)

        self.points = self.backend.asarray(
            points,
            dtype=self.backend.dtype_float(),
            device=device,
        )
        self.cells = self.backend.asarray(
            cells,
            dtype=self.backend.dtype_int(),
            device=device,
        )

        self._validate()

        self.point_data = MeshData(
            lambda: self.num_nodes,
            self.backend,
        )
        self.cell_data = MeshData(
            lambda: self.num_cells,
            self.backend,
        )

        self.topology = Topology(self)
        self.geometry = MeshGeometry(self)

    def _validate(self) -> None:
        if self.points.ndim != 2:
            raise ValueError(
                "points must have shape (num_nodes, geometric_dimension)"
            )

        if self.cells.ndim != 2:
            raise ValueError(
                "cells must have shape (num_cells, nodes_per_cell)"
            )

        if int(self.cells.shape[1]) != self.cell_type.num_nodes:
            raise ValueError(
                f"{self.cell_type.name} requires "
                f"{self.cell_type.num_nodes} nodes per cell"
            )

        cells_np = self.backend.to_numpy(self.cells)

        if cells_np.size:
            if int(cells_np.min()) < 0:
                raise ValueError(
                    "cell connectivity cannot contain negative ids"
                )

            if int(cells_np.max()) >= int(self.points.shape[0]):
                raise ValueError(
                    "cell connectivity contains invalid node ids"
                )

    @property
    def device(self):
        return self.backend.device_of(self.points)

    @property
    def num_nodes(self) -> int:
        return int(self.points.shape[0])

    @property
    def num_cells(self) -> int:
        return int(self.cells.shape[0])

    @property
    def geometric_dimension(self) -> int:
        return int(self.points.shape[1])

    @property
    def topological_dimension(self) -> int:
        return self.cell_type.topological_dimension

    @property
    def order(self) -> int:
        return self.cell_type.order

    def number_of_nodes(self) -> int:
        return self.num_nodes

    def number_of_edges(self) -> int:
        return self.topology.number_of_entities("edge")

    def number_of_cells(self) -> int:
        return self.num_cells

    def entity(self, entity: str):
        return self.topology.entities(entity)

    def connectivity(self, source: str, target: str):
        return self.topology.connectivity(source, target)

    def orientation(self, source: str, target: str):
        return self.topology.orientation(source, target)

    def cell_to_edge_sign(self):
        return self.topology.cell_to_edge_sign()

    def local_edge_nodes(self):
        return self.topology.local_edge_nodes()

    def local_numbering(self) -> dict[str, tuple]:
        """Describe the local node/edge/face numbering of this cell type."""
        return {
            "nodes": self.cell_type.local_node_ids(),
            "edges": self.cell_type.local_edges,
            "faces": self.cell_type.local_faces,
        }

    def boundary_entities(self, entity: str = "edge"):
        return self.topology.boundary_entities(entity)

    def measure(self, entity: str = "cell"):
        return self.geometry.measure(entity)

    def entity_barycenter(self, entity: str = "cell"):
        return self.geometry.barycenter(entity)

    def to_backend(
        self,
        backend: str | ArrayBackend,
        *,
        device=None,
    ) -> "Mesh":
        target = get_backend(backend)

        result = Mesh(
            target.asarray(
                self.backend.to_numpy(self.points),
                dtype=target.dtype_float(),
                device=device,
            ),
            target.asarray(
                self.backend.to_numpy(self.cells),
                dtype=target.dtype_int(),
                device=device,
            ),
            self.cell_type,
            backend=target,
            device=device,
        )

        for name, value in self.point_data.items():
            result.point_data[name] = target.asarray(
                self.backend.to_numpy(value),
                device=device,
            )

        for name, value in self.cell_data.items():
            result.cell_data[name] = target.asarray(
                self.backend.to_numpy(value),
                device=device,
            )

        return result

    def numpy(self) -> "Mesh":
        return self.to_backend("numpy")

    def torch(self, *, device=None) -> "Mesh":
        return self.to_backend("torch", device=device)


    def refine(self, method: str = "uniform", **kwargs):
        from ..meshing.refinement import refine
        return refine(self, method=method, **kwargs)

    def plot(self, **kwargs):
        from ..post import plot_mesh
        return plot_mesh(self, **kwargs)

    def viewer(self, **kwargs):
        from ..post import Viewer
        return Viewer(self, **kwargs)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"cell_type={self.cell_type.name!r}, "
            f"backend={self.backend.name!r}, "
            f"device={self.device!r}, "
            f"num_nodes={self.num_nodes}, "
            f"num_edges={self.number_of_edges()}, "
            f"num_cells={self.num_cells})"
        )

    def copy(self) -> "Mesh":
        result = Mesh(
            self.backend.copy(self.points),
            self.backend.copy(self.cells),
            self.cell_type,
            backend=self.backend,
            device=self.device,
        )

        for name, value in self.point_data.items():
            result.point_data[name] = self.backend.copy(value)

        for name, value in self.cell_data.items():
            result.cell_data[name] = self.backend.copy(value)

        return result
