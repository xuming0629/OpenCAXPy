import numpy as np
class DirichletBC:
    def __init__(self, field_or_space, value=0.0, dofs=None):
        self.space=getattr(field_or_space,"space",field_or_space)
        self.value=value
        self.dofs=np.asarray(self.space.boundary_dof() if dofs is None else dofs,int)
    def apply(self,A,b):
        A=np.array(A,float,copy=True); b=np.array(b,float,copy=True)
        vals=self.value
        if np.isscalar(vals): vals=np.full(len(self.dofs),float(vals))
        else: vals=np.asarray(vals,float).reshape(-1)
        b -= A[:,self.dofs]@vals
        for d,v in zip(self.dofs,vals):
            A[d,:]=0; A[:,d]=0; A[d,d]=1; b[d]=v
        return A,b
