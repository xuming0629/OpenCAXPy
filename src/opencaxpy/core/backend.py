#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : backend.py
# @Time          : 2026-07-28 10:21:20
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   :  
# @Company       : 2026 XuMing. All Rights Reserved.
"""



from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import numpy as np

from .errors import BackendError
from .registry import Registry


class ArrayBackend(ABC):
    """Backend protocol for array creation and elementary operations."""

    name: str

    @abstractmethod
    def asarray(
        self,
        value: Any,
        *,
        dtype: Any | None = None,
        device: Any | None = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def to_numpy(self, value: Any) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def copy(self, value: Any):
        raise NotImplementedError

    @abstractmethod
    def zeros(
        self,
        shape,
        *,
        dtype: Any | None = None,
        device: Any | None = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def full(
        self,
        shape,
        fill_value,
        *,
        dtype: Any | None = None,
        device: Any | None = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def arange(
        self,
        stop: int,
        *,
        dtype: Any | None = None,
        device: Any | None = None,
    ):
        raise NotImplementedError

    @abstractmethod
    def stack(self, values, *, axis: int = 0):
        raise NotImplementedError

    @abstractmethod
    def concatenate(self, values, *, axis: int = 0):
        raise NotImplementedError

    @abstractmethod
    def unique(self, value, *, axis: int | None = None):
        raise NotImplementedError

    @abstractmethod
    def norm(self, value, *, axis: int | None = None):
        raise NotImplementedError

    @abstractmethod
    def cross(self, a, b):
        raise NotImplementedError

    @abstractmethod
    def sum(self, value, *, axis: int | None = None):
        raise NotImplementedError

    @abstractmethod
    def mean(self, value, *, axis: int | None = None):
        raise NotImplementedError

    @abstractmethod
    def abs(self, value):
        raise NotImplementedError

    @abstractmethod
    def sqrt(self, value):
        raise NotImplementedError

    @abstractmethod
    def is_array(self, value: Any) -> bool:
        raise NotImplementedError

    @abstractmethod
    def dtype_float(self):
        raise NotImplementedError

    @abstractmethod
    def dtype_int(self):
        raise NotImplementedError

    @abstractmethod
    def device_of(self, value: Any):
        raise NotImplementedError


class NumPyBackend(ArrayBackend):
    name = "numpy"

    def asarray(self, value, *, dtype=None, device=None):
        if device not in (None, "cpu"):
            raise BackendError("NumPy backend only supports CPU")
        return np.ascontiguousarray(value, dtype=dtype)

    def to_numpy(self, value) -> np.ndarray:
        return np.asarray(value)

    def copy(self, value):
        return np.array(value, copy=True)

    def zeros(self, shape, *, dtype=None, device=None):
        if device not in (None, "cpu"):
            raise BackendError("NumPy backend only supports CPU")
        return np.zeros(shape, dtype=dtype)

    def full(self, shape, fill_value, *, dtype=None, device=None):
        if device not in (None, "cpu"):
            raise BackendError("NumPy backend only supports CPU")
        return np.full(shape, fill_value, dtype=dtype)

    def arange(self, stop, *, dtype=None, device=None):
        if device not in (None, "cpu"):
            raise BackendError("NumPy backend only supports CPU")
        return np.arange(stop, dtype=dtype)

    def stack(self, values, *, axis=0):
        return np.stack(tuple(values), axis=axis)

    def concatenate(self, values, *, axis=0):
        return np.concatenate(tuple(values), axis=axis)

    def unique(self, value, *, axis=None):
        return np.unique(value, axis=axis)

    def norm(self, value, *, axis=None):
        return np.linalg.norm(value, axis=axis)

    def cross(self, a, b):
        return np.cross(a, b)

    def sum(self, value, *, axis=None):
        return np.sum(value, axis=axis)

    def mean(self, value, *, axis=None):
        return np.mean(value, axis=axis)

    def abs(self, value):
        return np.abs(value)

    def sqrt(self, value):
        return np.sqrt(value)

    def is_array(self, value):
        return isinstance(value, np.ndarray)

    def dtype_float(self):
        return np.float64

    def dtype_int(self):
        return np.int64

    def device_of(self, value):
        return "cpu"


class TorchBackend(ArrayBackend):
    name = "torch"

    def _torch(self):
        try:
            import torch
        except ImportError as exc:
            raise BackendError(
                "PyTorch backend requires the optional 'torch' dependency"
            ) from exc
        return torch

    def _normalize_dtype(self, dtype):
        torch = self._torch()
        if dtype is None:
            return None
        mapping = {
            np.float32: torch.float32,
            np.float64: torch.float64,
            np.int32: torch.int32,
            np.int64: torch.int64,
            float: torch.float64,
            int: torch.int64,
        }
        return mapping.get(dtype, dtype)

    def asarray(self, value, *, dtype=None, device=None):
        torch = self._torch()
        dtype = self._normalize_dtype(dtype)

        if isinstance(value, torch.Tensor):
            result = value
            if dtype is not None:
                result = result.to(dtype=dtype)
            if device is not None:
                result = result.to(device=device)
            return result.contiguous()

        return torch.as_tensor(
            value,
            dtype=dtype,
            device=device,
        ).contiguous()

    def to_numpy(self, value) -> np.ndarray:
        torch = self._torch()
        if not isinstance(value, torch.Tensor):
            return np.asarray(value)
        return value.detach().cpu().numpy()

    def copy(self, value):
        return value.clone()

    def zeros(self, shape, *, dtype=None, device=None):
        torch = self._torch()
        return torch.zeros(
            shape,
            dtype=self._normalize_dtype(dtype),
            device=device,
        )

    def full(self, shape, fill_value, *, dtype=None, device=None):
        torch = self._torch()
        return torch.full(
            shape,
            fill_value,
            dtype=self._normalize_dtype(dtype),
            device=device,
        )

    def arange(self, stop, *, dtype=None, device=None):
        torch = self._torch()
        return torch.arange(
            stop,
            dtype=self._normalize_dtype(dtype),
            device=device,
        )

    def stack(self, values, *, axis=0):
        torch = self._torch()
        return torch.stack(tuple(values), dim=axis)

    def concatenate(self, values, *, axis=0):
        torch = self._torch()
        return torch.cat(tuple(values), dim=axis)

    def unique(self, value, *, axis=None):
        torch = self._torch()
        if axis is None:
            return torch.unique(value)
        return torch.unique(value, dim=axis)

    def norm(self, value, *, axis=None):
        torch = self._torch()
        if axis is None:
            return torch.linalg.vector_norm(value)
        return torch.linalg.vector_norm(value, dim=axis)

    def cross(self, a, b):
        torch = self._torch()
        return torch.linalg.cross(a, b, dim=-1)

    def sum(self, value, *, axis=None):
        if axis is None:
            return value.sum()
        return value.sum(dim=axis)

    def mean(self, value, *, axis=None):
        if axis is None:
            return value.mean()
        return value.mean(dim=axis)

    def abs(self, value):
        return value.abs()

    def sqrt(self, value):
        return value.sqrt()

    def is_array(self, value):
        torch = self._torch()
        return isinstance(value, torch.Tensor)

    def dtype_float(self):
        return self._torch().float64

    def dtype_int(self):
        return self._torch().int64

    def device_of(self, value):
        torch = self._torch()
        if isinstance(value, torch.Tensor):
            return value.device
        return None


BACKENDS: Registry[ArrayBackend] = Registry("array backend")
BACKENDS.register("numpy", NumPyBackend())
BACKENDS.register("torch", TorchBackend())


@dataclass(slots=True)
class BackendManager:
    default: str = "numpy"

    def get(self, backend: str | ArrayBackend | None = None) -> ArrayBackend:
        if backend is None:
            return BACKENDS.get(self.default)
        if isinstance(backend, str):
            return BACKENDS.get(backend)
        if isinstance(backend, ArrayBackend):
            return backend
        raise BackendError(
            "backend must be None, a backend name, or an ArrayBackend"
        )

    def set_default(self, backend: str) -> None:
        BACKENDS.get(backend)
        self.default = backend

    def names(self) -> tuple[str, ...]:
        return BACKENDS.names()


backend_manager = BackendManager()


def get_backend(
    backend: str | ArrayBackend | None = None,
) -> ArrayBackend:
    return backend_manager.get(backend)


def set_default_backend(name: str) -> None:
    backend_manager.set_default(name)
