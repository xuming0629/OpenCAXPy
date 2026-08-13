from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass
class Field:
    """A physical/result field independent from the visualization backend."""
    name: str
    values: object
    location: str = "point"  # point | cell
    kind: str = "scalar"     # scalar | vector | tensor
    components: tuple[str, ...] | None = None
    unit: str | None = None

    def __post_init__(self):
        if self.location not in {"point", "cell"}:
            raise ValueError("location must be 'point' or 'cell'")
        if self.kind not in {"scalar", "vector", "tensor"}:
            raise ValueError("kind must be scalar/vector/tensor")
        self.values = np.asarray(self.values)

    def component(self, component=None):
        v = np.asarray(self.values)
        if self.kind == "scalar" or component is None:
            return v.reshape(-1) if self.kind == "scalar" else v
        if component == "magnitude":
            if v.ndim != 2:
                raise ValueError(f"{self.name!r} must be 2-D for magnitude")
            return np.linalg.norm(v, axis=1)
        if isinstance(component, int):
            return v[:, component]
        if self.components is None:
            aliases = {"x": 0, "y": 1, "z": 2, "xx": 0, "yy": 1, "zz": 2, "xy": 3, "yz": 4, "xz": 5}
            if component not in aliases:
                raise KeyError(f"Unknown component {component!r}")
            return v[:, aliases[component]]
        try:
            idx = self.components.index(component)
        except ValueError as exc:
            raise KeyError(f"Field {self.name!r} has no component {component!r}") from exc
        return v[:, idx]
