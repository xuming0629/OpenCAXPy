from __future__ import annotations

import numpy as np


class RefinementDataTransfer:
    def transfer(self, source, result, context) -> None:
        target = result.mesh
        backend = source.backend

        if context.transfer_cell_data:
            parent = backend.to_numpy(result.parent_cell).astype(np.int64)
            for name, values in source.cell_data.items():
                source_values = backend.to_numpy(values)
                target.cell_data[name] = backend.asarray(
                    source_values[parent],
                    device=source.device,
                )

        if context.transfer_point_data:
            records = result.new_node_parent_entity
            for name, values in source.point_data.items():
                old = backend.to_numpy(values)
                rows = old.tolist()
                for record in records:
                    etype = record["parent_entity_type"]
                    entity = record["parent_entity"]
                    if etype in {"edge", "face"}:
                        value = old[list(entity)].mean(axis=0)
                    elif etype == "cell":
                        cell_id = entity[0]
                        node_ids = backend.to_numpy(source.cells[cell_id])
                        value = old[node_ids].mean(axis=0)
                    else:
                        raise ValueError(f"unknown parent entity type {etype}")
                    rows.append(np.asarray(value).tolist())
                target.point_data[name] = backend.asarray(
                    rows, device=source.device
                )
