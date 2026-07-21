from __future__ import annotations

import numpy as np

from opencaxpy.mesh.cell_type import CellType


def plot_mesh(mesh, *, show_node_ids=False, show_cell_ids=False, ax=None):
    if mesh.topological_dimension != 2:
        raise ValueError("plot_mesh currently supports only 2D meshes")

    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError("Install visualization extras: pip install -e '.[visual]'") from exc

    if ax is None:
        _, ax = plt.subplots()

    points = mesh.backend.to_numpy(mesh.points)
    cells = mesh.backend.to_numpy(mesh.cells)
    corners = cells[:, mesh.cell_type.corner_nodes]

    for cell_id, cell in enumerate(corners):
        polygon = np.concatenate((cell, cell[:1]))
        xy = points[polygon, :2]
        ax.plot(xy[:, 0], xy[:, 1])

        if show_cell_ids:
            center = points[cell, :2].mean(axis=0)
            ax.text(center[0], center[1], str(cell_id))

    if show_node_ids:
        for node_id, point in enumerate(points):
            ax.text(point[0], point[1], str(node_id))

    ax.set_aspect("equal")
    return ax
