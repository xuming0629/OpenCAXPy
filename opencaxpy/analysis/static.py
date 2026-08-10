import numpy as np
from ..assembly.dense import DenseAssembler
from ..solvers.linear.dense_direct import DenseDirectSolver
from ..results.result import Result
class StaticAnalysis:
    def __init__(self,model,solver=None,assembler=None):
        self.model=model; self.solver=solver or DenseDirectSolver(); self.assembler=assembler or DenseAssembler()
    def solve(self):
        K=self.assembler.assemble_structural(self.model.points,self.model.elements,self.model.ndof)
        F=self.model.load_vector(); U=np.zeros(self.model.ndof)
        c=np.array(sorted(self.model.constraints),int)
        f=np.setdiff1d(np.arange(self.model.ndof),c)
        if len(c): U[c]=[self.model.constraints[i] for i in c]
        rhs=F[f].copy()
        if len(c): rhs -= K[np.ix_(f,c)]@U[c]
        if len(f): U[f]=self.solver.solve(K[np.ix_(f,f)],rhs)
        R=K@U-F
        er={}
        for i,e in enumerate(self.model.elements):
            if hasattr(e,"recover"): er[i]=e.recover(self.model.points,U)
        r=Result(solution=U,reaction=R,metadata={"matrix":K,"rhs":F,"element_results":er})
        r.add_field("displacement",U,components=self.model.dofs_per_node)
        return r
