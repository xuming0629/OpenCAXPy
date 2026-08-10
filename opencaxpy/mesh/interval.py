import numpy as np
from .mesh import Mesh

class IntervalMesh(Mesh):
    def __init__(self, points, cells):
        p = np.asarray(points, dtype=float)
        if p.ndim == 1:
            p = p[:, None]
        super().__init__(p, cells, "line2")

    @classmethod
    def from_interval(cls, interval=(0.0, 1.0), n=10):
        a, b = interval
        points = np.linspace(a, b, n+1)[:, None]
        cells = np.column_stack(
            [np.arange(n), np.arange(1, n+1)]
        )
        return cls(points, cells)
