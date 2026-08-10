import numpy as np
def physical_gradients(coords, grad_ref):
    J=coords.T@grad_ref
    detJ=float(np.linalg.det(J))
    if abs(detJ)<1e-14: raise ValueError("degenerate element")
    return grad_ref@np.linalg.inv(J), detJ
