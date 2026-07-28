from __future__ import annotations

from collections.abc import MutableMapping, Iterator
from typing import Any


class MeshData(MutableMapping[str, Any]):
    """Validated data container attached to mesh entities."""

    def __init__(self, size_getter, backend) -> None:
        self._size_getter = size_getter
        self._backend = backend
        self._values: dict[str, Any] = {}

    def __getitem__(self, key: str):
        return self._values[key]

    def __setitem__(self, key: str, value) -> None:
        array = self._backend.asarray(value)

        if array.ndim == 0:
            raise ValueError(
                f"mesh data {key!r} must have at least one dimension"
            )

        expected = int(self._size_getter())
        if int(array.shape[0]) != expected:
            raise ValueError(
                f"mesh data {key!r} first dimension must be {expected}, "
                f"got {array.shape[0]}"
            )

        self._values[key] = array

    def __delitem__(self, key: str) -> None:
        del self._values[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    def copy_to(self, backend, device=None) -> "MeshData":
        result = MeshData(self._size_getter, backend)

        for name, value in self._values.items():
            result._values[name] = backend.asarray(
                self._backend.to_numpy(value),
                device=device,
            )

        return result
