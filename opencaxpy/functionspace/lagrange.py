import numpy as np
from .dof import DofManager
class LagrangeSpace:
    def __init__(self, mesh, degree=1, components=1):
        if degree != 1: raise NotImplementedError("v1.1 implements P1 only")
        self.mesh=mesh; self.degree=degree; self.components=components
        self.dof=DofManager(mesh,components)
    @property
    def number_of_global_dofs(self): return self.dof.number_of_dofs
    def cell_to_dof(self): return self.dof.cell_to_dof()
    def boundary_dof(self):
        nodes=self.mesh.boundary_node_index()
        if self.components==1: return nodes
        ids=[]
        for n in nodes:
            ids += [self.dof.node_to_dof(n,c) for c in range(self.components)]
        return np.asarray(ids,int)
