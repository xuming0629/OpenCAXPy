from ..discretization.fem.form.bilinear import BilinearForm
from ..discretization.fem.form.linear import LinearForm
from ..discretization.fem.integrator.diffusion import DiffusionIntegrator
from ..discretization.fem.integrator.source import SourceIntegrator
from ..assembly.dense import DenseAssembler
from ..boundary.dirichlet import DirichletBC
from ..solvers.linear.dense_direct import DenseDirectSolver
from ..results.result import Result

class SteadyAnalysis:
    def __init__(self,problem,solver=None,assembler=None):
        self.problem=problem; self.solver=solver or DenseDirectSolver(); self.assembler=assembler or DenseAssembler()
    def solve_poisson(self,field_name,physics,dirichlet=0.0):
        field=self.problem.fields[field_name]
        a=BilinearForm(field.space).add_integrator(DiffusionIntegrator(physics.diffusion))
        l=LinearForm(field.space).add_integrator(SourceIntegrator(physics.source))
        A0=self.assembler.assemble_bilinear(a); b0=self.assembler.assemble_linear(l)
        A,b=DirichletBC(field,dirichlet).apply(A0,b0)
        u=self.solver.solve(A,b); field.values=u
        r=Result(solution=u,reaction=A0@u-b0,metadata={"matrix":A0,"rhs":b0})
        r.add_field(field.name,u,components=field.components)
        return r
