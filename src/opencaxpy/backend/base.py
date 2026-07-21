from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Sequence


class ArrayBackend(ABC):
    name: str

    @abstractmethod
    def asarray(self, data: Any, *, dtype=None, device=None):
        raise NotImplementedError

    @abstractmethod
    def zeros(self, shape: Sequence[int], *, dtype=None, device=None):
        raise NotImplementedError

    @abstractmethod
    def arange(self, stop: int, *, dtype=None, device=None):
        raise NotImplementedError

    @abstractmethod
    def concatenate(self, arrays, axis=0):
        raise NotImplementedError

    @abstractmethod
    def stack(self, arrays, axis=0):
        raise NotImplementedError

    @abstractmethod
    def to_numpy(self, array):
        raise NotImplementedError

    @abstractmethod
    def device_of(self, array) -> str:
        raise NotImplementedError

    @abstractmethod
    def dtype_of(self, array):
        raise NotImplementedError
