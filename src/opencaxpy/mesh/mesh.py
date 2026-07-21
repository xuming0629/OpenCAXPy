from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from opencaxpy.backend import backend_manager
from .cell_type import CellType


@dataclass
class Mesh:
    points: Any
    cells: Any
    cell_type: CellType | str
    backend_name: str | None = None
    device_hint: str | None = None
    point_data: dict[str, Any] = field(default_factory=dict)
    cell_data: dict[str, Any] = field(default_factory=dict)
    field_data: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.cell_type = CellType(self.cell_type)
        self.backend = backend_manager.get(self.backend_name)

        self.points = self.backend.asarray(
            self.points,
            dtype=self._float_dtype(),
            device=self.device_hint,
        )
        self.cells = self.backend.asarray(
            self.cells,
            dtype=self._index_dtype(),
            device=self.device_hint,
        )

        if self.points.ndim != 2:
            raise ValueError("points must have shape [num_nodes, geometric_dimension]")
        if self.cells.ndim != 2:
            raise ValueError("cells must have shape [num_cells, nodes_per_cell]")
        if self.cells.shape[1] != self.cell_type.num_nodes:
            raise ValueError(
                f"{self.cell_type.value} requires {self.cell_type.num_nodes} nodes "
                f"per cell, got {self.cells.shape[1]}"
            )
        if self.points.shape[1] < self.cell_type.dimension:
            raise ValueError(
                "geometric dimension cannot be smaller than topological dimension"
            )

        self._topology = None

    def _float_dtype(self):
        if self.backend.name == "numpy":
            return np.float64
        import torch
        return torch.float64

    def _index_dtype(self):
        if self.backend.name == "numpy":
            return np.int64
        import torch
        return torch.int64

    @property
    def backend_name_resolved(self) -> str:
        return self.backend.name

    @property
    def device(self) -> str:
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
        return self.cell_type.dimension

    @property
    def topology(self):
        if self._topology is None:
            from .topology import create_topology
            self._topology = create_topology(self)
        return self._topology.build()

    def invalidate_topology(self) -> None:
        self._topology = None

    def cell_points(self):
        return self.points[self.cells]

    def copy(self):
        points = self.backend.asarray(
            self.backend.to_numpy(self.points).copy(),
            dtype=self.backend.dtype_of(self.points),
            device=self.device,
        )
        cells = self.backend.asarray(
            self.backend.to_numpy(self.cells).copy(),
            dtype=self.backend.dtype_of(self.cells),
            device=self.device,
        )
        return Mesh(
            points,
            cells,
            self.cell_type,
            backend_name=self.backend.name,
            device_hint=self.device,
            point_data=dict(self.point_data),
            cell_data=dict(self.cell_data),
            field_data=dict(self.field_data),
        )

    def to(self, *, backend: str | None = None, device: str | None = None):
        target = backend_manager.get(backend or self.backend.name)
        target_device = device or ("cpu" if target.name == "numpy" else self.device)
        return Mesh(
            target.asarray(
                self.backend.to_numpy(self.points),
                dtype=(np.float64 if target.name == "numpy" else None),
                device=target_device,
            ),
            target.asarray(
                self.backend.to_numpy(self.cells),
                dtype=(np.int64 if target.name == "numpy" else None),
                device=target_device,
            ),
            self.cell_type,
            backend_name=target.name,
            device_hint=target_device,
            point_data={
                k: target.asarray(self.backend.to_numpy(v), device=target_device)
                for k, v in self.point_data.items()
            },
            cell_data={
                k: target.asarray(self.backend.to_numpy(v), device=target_device)
                for k, v in self.cell_data.items()
            },
            field_data=dict(self.field_data),
        )

    def validate(self, *, raise_on_error: bool = False) -> dict:
        points = self.backend.to_numpy(self.points)
        cells = self.backend.to_numpy(self.cells)

        errors = []
        if not np.isfinite(points).all():
            errors.append("points contain NaN or infinity")
        if cells.size and cells.min() < 0:
            errors.append("cells contain negative node indices")
        if cells.size and cells.max() >= self.num_nodes:
            errors.append("cells reference nodes outside the points array")
        repeated = np.any(
            np.apply_along_axis(lambda row: len(set(row.tolist())) != len(row), 1, cells)
        ) if self.num_cells else False
        if repeated:
            errors.append("one or more cells contain repeated node indices")

        measures = self.measure()
        if np.any(measures <= 0.0):
            errors.append("one or more cells are degenerate or inverted")

        report = {
            "is_valid": not errors,
            "errors": errors,
            "num_nodes": self.num_nodes,
            "num_cells": self.num_cells,
            "cell_type": self.cell_type.value,
        }
        if errors and raise_on_error:
            raise ValueError("; ".join(errors))
        return report

    def measure(self):
        points = self.backend.to_numpy(self.points)
        cells = self.backend.to_numpy(self.cells)
        corners = cells[:, self.cell_type.corner_nodes]
        x = points[corners]

        if self.cell_type in (CellType.TRIANGLE3, CellType.TRIANGLE6):
            a = x[:, 1] - x[:, 0]
            b = x[:, 2] - x[:, 0]
            if self.geometric_dimension == 2:
                return 0.5 * np.abs(a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0])
            return 0.5 * np.linalg.norm(np.cross(a, b), axis=1)

        if self.cell_type in (CellType.QUAD4, CellType.QUAD8, CellType.QUAD9):
            tri1 = x[:, [0, 1, 2]]
            tri2 = x[:, [0, 2, 3]]
            def area(tri):
                a = tri[:, 1] - tri[:, 0]
                b = tri[:, 2] - tri[:, 0]
                if self.geometric_dimension == 2:
                    return 0.5 * np.abs(a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0])
                return 0.5 * np.linalg.norm(np.cross(a, b), axis=1)
            return area(tri1) + area(tri2)

        if self.cell_type in (CellType.TETRA4, CellType.TETRA10):
            a = x[:, 1] - x[:, 0]
            b = x[:, 2] - x[:, 0]
            c = x[:, 3] - x[:, 0]
            return np.abs(np.einsum("ij,ij->i", np.cross(a, b), c)) / 6.0

        if self.cell_type == CellType.HEXA8:
            # Six-tetra decomposition, suitable for affine structured Hexa8 cells.
            tet_local = np.asarray([
                [0, 1, 2, 6],
                [0, 2, 3, 6],
                [0, 3, 7, 6],
                [0, 7, 4, 6],
                [0, 4, 5, 6],
                [0, 5, 1, 6],
            ], dtype=np.int64)
            total = np.zeros(self.num_cells, dtype=np.float64)
            for tet in tet_local:
                t = x[:, tet]
                a = t[:, 1] - t[:, 0]
                b = t[:, 2] - t[:, 0]
                c = t[:, 3] - t[:, 0]
                total += np.abs(np.einsum("ij,ij->i", np.cross(a, b), c)) / 6.0
            return total

        raise NotImplementedError(f"measure is not implemented for {self.cell_type}")

    def total_measure(self) -> float:
        return float(self.measure().sum())

    def to_order(self, order: int, *, quad_center: bool = True):
        if order == self.cell_type.order:
            return self.copy()
        if order != 2 or self.cell_type.order != 1:
            raise NotImplementedError("Only first-order to second-order conversion is implemented")

        from .order_conversion import to_second_order
        return to_second_order(self, quad_center=quad_center)


    def write_vtu(self, filename):
        from opencaxpy.post import VtkExporter
        return VtkExporter.write(self, filename)

    def show(self, *, scalars=None, show_edges=True, show_node_ids=False, show_cell_ids=False):
        from opencaxpy.post import VtkViewer
        return VtkViewer.show(self, scalars=scalars, show_edges=show_edges, show_node_ids=show_node_ids, show_cell_ids=show_cell_ids)

    def __repr__(self) -> str:
        return (
            f"Mesh(cell_type='{self.cell_type.value}', "
            f"num_nodes={self.num_nodes}, num_cells={self.num_cells}, "
            f"backend='{self.backend.name}', device='{self.device}')"
        )
