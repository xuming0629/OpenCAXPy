from enum import Enum
import numpy as np
class DofEntity(str, Enum):
    VERTEX="vertex"; EDGE="edge"; FACE="face"; CELL="cell"

class DofManager:
    def __init__(self, mesh, components=1, entity=DofEntity.VERTEX):
        self.mesh=mesh; self.components=int(components); self.entity=entity
        if entity != DofEntity.VERTEX:
            raise NotImplementedError("v1.1 reserves edge/face/cell DOFs")
    @property
    def number_of_dofs(self): return self.mesh.number_of_nodes()*self.components
    def node_to_dof(self,n,c=0): return int(n)*self.components+int(c)
    def cell_to_dof(self):
        if self.components==1: return self.mesh.cells.copy()
        out=[]
        for cell in self.mesh.cells:
            row=[]
            for n in cell:
                row += [self.node_to_dof(n,c) for c in range(self.components)]
            out.append(row)
        return np.asarray(out,int)
