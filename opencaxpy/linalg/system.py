from dataclasses import dataclass
import numpy as np
@dataclass
class LinearSystem:
    A: np.ndarray
    b: np.ndarray
