from __future__ import annotations

import numpy as np

from .base import ArrayBackend


class TorchBackend(ArrayBackend):
    name = "torch"

    @staticmethod
    def _torch():
        try:
            import torch
        except ImportError as exc:
            raise ImportError(
                "PyTorch is not installed. Run: pip install -e '.[torch]'"
            ) from exc
        return torch

    def asarray(self, data, *, dtype=None, device=None):
        torch = self._torch()
        if isinstance(data, torch.Tensor):
            return data.to(dtype=dtype or data.dtype, device=device or data.device)
        return torch.as_tensor(data, dtype=dtype, device=device or "cpu")

    def zeros(self, shape, *, dtype=None, device=None):
        torch = self._torch()
        return torch.zeros(tuple(shape), dtype=dtype, device=device or "cpu")

    def arange(self, stop, *, dtype=None, device=None):
        torch = self._torch()
        return torch.arange(stop, dtype=dtype, device=device or "cpu")

    def concatenate(self, arrays, axis=0):
        torch = self._torch()
        return torch.cat(tuple(arrays), dim=axis)

    def stack(self, arrays, axis=0):
        torch = self._torch()
        return torch.stack(tuple(arrays), dim=axis)

    def to_numpy(self, array):
        return array.detach().cpu().numpy()

    def device_of(self, array) -> str:
        return str(array.device)

    def dtype_of(self, array):
        return array.dtype
