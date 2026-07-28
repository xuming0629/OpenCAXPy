from __future__ import annotations


class MeshGeneratorRegistry:
    def __init__(self) -> None:
        self._items = {}

    def register(self, generator, *, replace: bool = False):
        name = generator.name
        if name in self._items and not replace:
            raise KeyError(f"mesh generator already registered: {name!r}")
        self._items[name] = generator
        return generator

    def get(self, name: str):
        try:
            return self._items[name]
        except KeyError as exc:
            raise KeyError(
                f"unknown mesh generator {name!r}; available={self.names()}"
            ) from exc

    def create(self, name: str, **kwargs):
        return self.get(name).generate(**kwargs)

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._items))


mesh_generator_registry = MeshGeneratorRegistry()
