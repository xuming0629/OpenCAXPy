from __future__ import annotations

from .base import ArrayBackend
from .numpy_backend import NumPyBackend
from .torch_backend import TorchBackend


class BackendManager:
    def __init__(self):
        self._backends: dict[str, ArrayBackend] = {
            "numpy": NumPyBackend(),
            "torch": TorchBackend(),
        }
        self._default = "numpy"

    @property
    def default_name(self) -> str:
        return self._default

    def register(self, name: str, backend: ArrayBackend) -> None:
        if not name:
            raise ValueError("Backend name cannot be empty")
        self._backends[name] = backend

    def set_default(self, name: str) -> None:
        self.get(name)
        self._default = name

    def get(self, name: str | None = None) -> ArrayBackend:
        key = name or self._default
        try:
            return self._backends[key]
        except KeyError as exc:
            available = ", ".join(sorted(self._backends))
            raise ValueError(
                f"Unknown backend '{key}'. Available backends: {available}"
            ) from exc


backend_manager = BackendManager()


def set_default_backend(name: str) -> None:
    backend_manager.set_default(name)
