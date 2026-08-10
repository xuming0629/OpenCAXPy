import numpy as np
class DenseAssembler:
    def assemble_bilinear(self,form):
        s=form.space; A=np.zeros((s.number_of_global_dofs,s.number_of_global_dofs))
        c2d=s.cell_to_dof()
        for ci in range(s.mesh.number_of_cells()):
            local=None
            for integ in form.integrators:
                k=integ.cell_matrix(s.mesh,ci); local=k if local is None else local+k
            d=c2d[ci]; A[np.ix_(d,d)] += local
        return A
    def assemble_linear(self,form):
        s=form.space; b=np.zeros(s.number_of_global_dofs); c2d=s.cell_to_dof()
        for ci in range(s.mesh.number_of_cells()):
            local=None
            for integ in form.integrators:
                v=integ.cell_vector(s.mesh,ci); local=v if local is None else local+v
            b[c2d[ci]] += local
        return b
    def assemble_structural(self,points,elements,ndof):
        K=np.zeros((ndof,ndof))
        for e in elements:
            d=e.dof_indices()
            K[np.ix_(d,d)] += e.stiffness_matrix(points)
        return K
