from dataclasses import dataclass
import numpy as np
@dataclass
class Field:
    name: str
    space: object
    values: np.ndarray | None = None
    @property
    def components(self): return self.space.components
    def zeros(self):
        self.values = np.zeros(self.space.number_of_global_dofs)
        return self.values
