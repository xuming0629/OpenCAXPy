from __future__ import annotations
from abc import ABC, abstractmethod


class Plot(ABC):
    title: str | None = None

    @property
    @abstractmethod
    def backend(self) -> str: ...

    @abstractmethod
    def render(self, context): ...
