from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CSRConnectivity:
    offsets: object
    indices: object

    def row(self, index: int):
        begin = int(self.offsets[index])
        end = int(self.offsets[index + 1])
        return self.indices[begin:end]

    @property
    def num_rows(self) -> int:
        return len(self.offsets) - 1
