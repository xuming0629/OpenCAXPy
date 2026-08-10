from ..interpolation.lagrange_p1 import triangle_grad_reference, tetra_grad_reference
from ..mapping.isoparametric import physical_gradients
class DiffusionIntegrator:
    def __init__(self, coefficient=1.0): self.coefficient=coefficient
    def cell_matrix(self, mesh, ci):
        coords=mesh.cell_coordinates(ci)
        if mesh.cell_type=="triangle3":
            grad_ref=triangle_grad_reference(); refm=0.5
        elif mesh.cell_type=="tetra4":
            grad_ref=tetra_grad_reference(); refm=1/6
        else:
            raise NotImplementedError(mesh.cell_type)
        grad,detJ=physical_gradients(coords,grad_ref)
        xbar=coords.mean(axis=0)
        k=self.coefficient(xbar) if callable(self.coefficient) else self.coefficient
        return float(k)*(grad@grad.T)*abs(detJ)*refm
