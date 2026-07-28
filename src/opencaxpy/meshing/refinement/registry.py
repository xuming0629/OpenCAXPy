from __future__ import annotations


class RefinementRegistry:
    def __init__(self) -> None:
        self._items = {}

    def register(self, refiner, *, replace: bool = False):
        for cell_type in refiner.supported_cell_types:
            key = (cell_type, refiner.method)
            if key in self._items and not replace:
                raise KeyError(f"refiner already registered: {key}")
            self._items[key] = refiner
        return refiner

    def get(self, cell_type: str, method: str):
        key = (cell_type, method)
        try:
            return self._items[key]
        except KeyError as exc:
            raise KeyError(
                f"no refiner for {cell_type!r}/{method!r}; "
                f"available={self.methods(cell_type)}"
            ) from exc

    def methods(self, cell_type: str) -> tuple[str, ...]:
        return tuple(sorted(
            method for (ctype, method) in self._items if ctype == cell_type
        ))

    def entries(self) -> tuple[tuple[str, str], ...]:
        return tuple(sorted(self._items))


refinement_registry = RefinementRegistry()
