from __future__ import annotations

import numpy as np

from .base import ArrayBackend


class NumPyBackend(ArrayBackend):
    name = "numpy"

    def asarray(self, data, *, dtype=None, device=None):
        if device not in (None, "cpu"):
            raise ValueError("NumPy backend only supports device='cpu'")
        return np.asarray(data, dtype=dtype)

    def zeros(self, shape, *, dtype=None, device=None):
        if device not in (None, "cpu"):
            raise ValueError("NumPy backend only supports device='cpu'")
        return np.zeros(tuple(shape), dtype=dtype)

    def arange(self, stop, *, dtype=None, device=None):
        if device not in (None, "cpu"):
            raise ValueError("NumPy backend only supports device='cpu'")
        return np.arange(stop, dtype=dtype)

    def concatenate(self, arrays, axis=0):
        return np.concatenate(tuple(arrays), axis=axis)

    def stack(self, arrays, axis=0):
        return np.stack(tuple(arrays), axis=axis)

    def to_numpy(self, array):
        return np.asarray(array)

    def device_of(self, array) -> str:
        return "cpu"

    def dtype_of(self, array):
        return array.dtype
