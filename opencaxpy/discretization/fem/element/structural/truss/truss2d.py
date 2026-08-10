from dataclasses import dataclass
import numpy as np
@dataclass
class Truss2D:
    node_ids: tuple[int,int]
    E: float
    A: float
    dofs_per_node=2
    def dof_indices(self):
        i,j=self.node_ids
        return np.array([2*i,2*i+1,2*j,2*j+1])
    def stiffness_matrix(self, points):
        i,j=self.node_ids
        d=points[j]-points[i]; L=float(np.linalg.norm(d)); c,s=d[0]/L,d[1]/L
        return self.E*self.A/L*np.array([
            [c*c,c*s,-c*c,-c*s],[c*s,s*s,-c*s,-s*s],
            [-c*c,-c*s,c*c,c*s],[-c*s,-s*s,c*s,s*s]
        ])
    def recover(self, points, U):
        i,j=self.node_ids
        d=points[j]-points[i]; L=float(np.linalg.norm(d)); c,s=d[0]/L,d[1]/L
        ue=U[self.dof_indices()]
        strain=float(np.array([-c,-s,c,s])@ue/L)
        stress=self.E*strain
        return {"strain":strain,"stress":stress,"axial_force":self.A*stress}
