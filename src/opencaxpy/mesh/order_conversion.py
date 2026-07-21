from __future__ import annotations

import numpy as np

from .cell_type import CellType
from .mesh import Mesh


def _edge_nodes(mesh):
    topology = mesh.topology
    points = mesh.backend.to_numpy(mesh.points)
    edges = mesh.backend.to_numpy(topology.edges).astype(np.int64, copy=False)
    edge_points = 0.5 * (points[edges[:, 0]] + points[edges[:, 1]])
    edge_node_ids = np.arange(edges.shape[0], dtype=np.int64) + mesh.num_nodes
    return edges, edge_points, edge_node_ids


def to_second_order(mesh: Mesh, *, quad_center: bool = True) -> Mesh:
    points = mesh.backend.to_numpy(mesh.points)
    cells = mesh.backend.to_numpy(mesh.cells).astype(np.int64, copy=False)
    topology = mesh.topology
    cell_to_edge = mesh.backend.to_numpy(topology.cell_to_edge).astype(np.int64, copy=False)

    _, edge_points, edge_node_ids = _edge_nodes(mesh)
    new_points = np.concatenate((points, edge_points), axis=0)
    edge_nodes_per_cell = edge_node_ids[cell_to_edge]

    if mesh.cell_type == CellType.TRIANGLE3:
        new_cells = np.concatenate((cells, edge_nodes_per_cell), axis=1)
        target = CellType.TRIANGLE6

    elif mesh.cell_type == CellType.QUAD4:
        if quad_center:
            centers = points[cells].mean(axis=1)
            center_ids = (
                np.arange(mesh.num_cells, dtype=np.int64)
                + new_points.shape[0]
            )
            new_points = np.concatenate((new_points, centers), axis=0)
            new_cells = np.concatenate(
                (cells, edge_nodes_per_cell, center_ids[:, None]),
                axis=1,
            )
            target = CellType.QUAD9
        else:
            new_cells = np.concatenate((cells, edge_nodes_per_cell), axis=1)
            target = CellType.QUAD8

    elif mesh.cell_type == CellType.TETRA4:
        new_cells = np.concatenate((cells, edge_nodes_per_cell), axis=1)
        target = CellType.TETRA10

    else:
        raise NotImplementedError(
            f"Second-order conversion is not implemented for {mesh.cell_type.value}"
        )

    return Mesh(
        new_points,
        new_cells,
        target,
        backend_name=mesh.backend.name,
        device_hint=mesh.device,
    )
