import numpy as np
from opencaxpy import TriangleMesh,LagrangeSpace,Field,Model,Problem,PoissonPhysics,SteadyAnalysis

def src(x):
    return 2*np.pi**2*np.sin(np.pi*x[0])*np.sin(np.pi*x[1])

mesh=TriangleMesh.from_box((0,1,0,1),20,20)
problem=Problem(Model(mesh=mesh))
problem.add_field(Field("u",LagrangeSpace(mesh)))
r=SteadyAnalysis(problem).solve_poisson("u",PoissonPhysics(1.0,src),0.0)
ue=np.sin(np.pi*mesh.points[:,0])*np.sin(np.pi*mesh.points[:,1])
print("RMS =",np.sqrt(np.mean((r.field("u").values-ue)**2)))
