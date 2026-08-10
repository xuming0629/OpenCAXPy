import numpy as np
def triangle_grad_reference():
    return np.array([[-1.,-1.],[1.,0.],[0.,1.]])
def tetra_grad_reference():
    return np.array([[-1.,-1.,-1.],[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]])
