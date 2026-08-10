from dataclasses import dataclass
import numpy as np
@dataclass
class TimoshenkoBeam2D:
    node_ids: tuple[int,int]
    E: float
    G: float
    A: float
    I: float
    kappa: float=5/6
    dofs_per_node=3
    def _geo(self,points):
        i,j=self.node_ids
        d=points[j]-points[i]; L=float(np.linalg.norm(d))
        return L,d[0]/L,d[1]/L
    def dof_indices(self):
        i,j=self.node_ids
        return np.array([3*i,3*i+1,3*i+2,3*j,3*j+1,3*j+2])
    def local_stiffness(self,points):
        L,_,_=self._geo(points)
        phi=12*self.E*self.I/(self.kappa*self.G*self.A*L**2); psi=1/(1+phi)
        EA=self.E*self.A/L
        k1=12*self.E*self.I*psi/L**3
        k2=6*self.E*self.I*psi/L**2
        k3=(4+phi)*self.E*self.I*psi/L
        k4=(2-phi)*self.E*self.I*psi/L
        return np.array([
            [EA,0,0,-EA,0,0],[0,k1,k2,0,-k1,k2],[0,k2,k3,0,-k2,k4],
            [-EA,0,0,EA,0,0],[0,-k1,-k2,0,k1,-k2],[0,k2,k4,0,-k2,k3]
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
