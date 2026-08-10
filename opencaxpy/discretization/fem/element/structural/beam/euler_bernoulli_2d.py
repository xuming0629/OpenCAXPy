from dataclasses import dataclass
import numpy as np
@dataclass
class EulerBernoulliBeam2D:
    node_ids: tuple[int,int]
    E: float
    A: float
    I: float
    dofs_per_node=3
    def _geo(self,points):
        i,j=self.node_ids
        d=points[j]-points[i]; L=float(np.linalg.norm(d))
        return L,d[0]/L,d[1]/L
    def dof_indices(self):
        i,j=self.node_ids
        return np.array([3*i,3*i+1,3*i+2,3*j,3*j+1,3*j+2])
    def local_stiffness(self,points):
        L,_,_=self._geo(points); EA=self.E*self.A/L; EI=self.E*self.I
        return np.array([
            [EA,0,0,-EA,0,0],
            [0,12*EI/L**3,6*EI/L**2,0,-12*EI/L**3,6*EI/L**2],
            [0,6*EI/L**2,4*EI/L,0,-6*EI/L**2,2*EI/L],
            [-EA,0,0,EA,0,0],
            [0,-12*EI/L**3,-6*EI/L**2,0,12*EI/L**3,-6*EI/L**2],
            [0,6*EI/L**2,2*EI/L,0,-6*EI/L**2,4*EI/L]
        ])
    def transformation(self,points):
        _,c,s=self._geo(points)
        return np.array([
            [c,s,0,0,0,0],[-s,c,0,0,0,0],[0,0,1,0,0,0],
            [0,0,0,c,s,0],[0,0,0,-s,c,0],[0,0,0,0,0,1]
        ])
    def stiffness_matrix(self,points):
        T=self.transformation(points)
        return T.T@self.local_stiffness(points)@T
