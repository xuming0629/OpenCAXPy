from __future__ import annotations

from abc import ABC, abstractmethod


class MeshGenerator(ABC):
    name: str

    @abstractmethod
    def generate(self, **kwargs):
        raise NotImplementedError
