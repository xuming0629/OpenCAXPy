import numpy as np
class NumPyBackend:
    name = "numpy"
    def asarray(self, x, dtype=None): return np.asarray(x, dtype=dtype)
    def zeros(self, shape, dtype=float): return np.zeros(shape, dtype=dtype)
    def ones(self, shape, dtype=float): return np.ones(shape, dtype=dtype)
