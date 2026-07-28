from __future__ import annotations

import numpy as np


def backend_int(mesh, values):
    return mesh.backend.asarray(
        values,
        dtype=mesh.backend.dtype_int(),
        device=mesh.device,
    )


def marked_cell_ids(mesh, marked_cells):
    if marked_cells is None:
        return set(range(mesh.num_cells))
    values = np.asarray(marked_cells)
    if values.dtype == bool:
        if values.shape != (mesh.num_cells,):
            raise ValueError("boolean marked_cells must match num_cells")
        return set(np.flatnonzero(values).tolist())
    ids = {int(v) for v in values.reshape(-1)}
    if any(v < 0 or v >= mesh.num_cells for v in ids):
        raise IndexError("marked cell id out of range")
    return ids
