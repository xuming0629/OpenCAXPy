from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..core import TopologyError


@dataclass(slots=True)
class Connectivity:
    """Compressed sparse-row entity connectivity."""

    offsets: object
    indices: object
    source_size: int
    target_size: int
    source_name: str
    target_name: str
    backend: object

    def __post_init__(self) -> None:
        offsets_np = self.backend.to_numpy(self.offsets)
        indices_np = self.backend.to_numpy(self.indices)

        if offsets_np.ndim != 1 or indices_np.ndim != 1:
            raise TopologyError(
                "connectivity offsets and indices must be one-dimensional"
            )

        if len(offsets_np) != self.source_size + 1:
            raise TopologyError(
                "offset count must equal source_size + 1"
            )

        if offsets_np[0] != 0:
            raise TopologyError("first connectivity offset must be zero")

        if offsets_np[-1] != len(indices_np):
            raise TopologyError(
                "last connectivity offset must equal index count"
            )

    def __len__(self) -> int:
        return self.source_size

    def __getitem__(self, source_id: int):
        start = int(self.backend.to_numpy(self.offsets)[source_id])
        end = int(self.backend.to_numpy(self.offsets)[source_id + 1])
        return self.indices[start:end]

    def row(self, source_id: int):
        return self[source_id]

    def to_lists(self) -> list[list[int]]:
        offsets = self.backend.to_numpy(self.offsets)
        indices = self.backend.to_numpy(self.indices)

        return [
            indices[offsets[i]:offsets[i + 1]].astype(int).tolist()
            for i in range(self.source_size)
        ]

    @classmethod
    def from_lists(
        cls,
        rows,
        *,
        source_name: str,
        target_name: str,
        target_size: int,
        backend,
        device=None,
    ) -> "Connectivity":
        offsets = [0]
        indices: list[int] = []

        for row in rows:
            indices.extend(int(value) for value in row)
            offsets.append(len(indices))

        return cls(
            offsets=backend.asarray(
                offsets,
                dtype=backend.dtype_int(),
                device=device,
            ),
            indices=backend.asarray(
                indices,
                dtype=backend.dtype_int(),
                device=device,
            ),
            source_size=len(rows),
            target_size=target_size,
            source_name=source_name,
            target_name=target_name,
            backend=backend,
        )

    @classmethod
    def from_dense(
        cls,
        values,
        *,
        source_name: str,
        target_name: str,
        target_size: int,
        backend,
        device=None,
    ) -> "Connectivity":
        array = backend.to_numpy(values)

        if array.ndim != 2:
            raise TopologyError(
                "dense connectivity must be two-dimensional"
            )

        return cls.from_lists(
            array.tolist(),
            source_name=source_name,
            target_name=target_name,
            target_size=target_size,
            backend=backend,
            device=device,
        )
