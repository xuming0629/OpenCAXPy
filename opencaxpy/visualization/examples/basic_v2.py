import numpy as np
from dataclasses import dataclass
from opencaxpy.visualization import Field, Solution, MeshPlot, SolutionPlot, ConvergencePlot, show

@dataclass
class DemoMesh:
    points: np.ndarray
    cells: np.ndarray
    cell_type: str = "triangle3"
    geometric_dimension: int = 2
    topological_dimension: int = 2

mesh=DemoMesh(
    points=np.array([[0.,0.],[1.,0.],[1.,1.],[0.,1.]]),
    cells=np.array([[0,1,2],[0,2,3]],dtype=int),
)
sol=Solution()
sol.add_field(Field("displacement",np.array([[0,0],[.02,0],[.02,.03],[0,.03]]),kind="vector",components=("x","y")))
sol.add_field(Field("u",np.array([0.,.3,1.,.4]),kind="scalar"))
h=np.array([.5,.25,.125,.0625]); err=0.08*h**2

show([
    MeshPlot(mesh,title="Mesh"),
    SolutionPlot(mesh,sol,field="u",deformation="displacement",scale="auto",title="Numerical solution"),
    ConvergencePlot(h,err,expected_order=2,title="Error order"),
],layout=(1,3))
