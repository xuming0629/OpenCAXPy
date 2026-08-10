import numpy as np
from opencaxpy import TriangleMesh,LagrangeSpace,Field,Model,Problem,PoissonPhysics,SteadyAnalysis
def test_poisson():
    def src(x): return 2*np.pi**2*np.sin(np.pi*x[0])*np.sin(np.pi*x[1])
    m=TriangleMesh.from_box((0,1,0,1),12,12)
    p=Problem(Model(mesh=m)); p.add_field(Field("u",LagrangeSpace(m)))
    r=SteadyAnalysis(p).solve_poisson("u",PoissonPhysics(1.0,src),0.0)
    ue=np.sin(np.pi*m.points[:,0])*np.sin(np.pi*m.points[:,1])
    assert np.sqrt(np.mean((r.field("u").values-ue)**2))<0.02
