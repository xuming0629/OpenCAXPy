import numpy as np
from opencaxpy import StructuralModel,Truss2D,StaticAnalysis
p=np.array([[0,0],[2,0],[1,1.5]],float)
m=StructuralModel(p,2)
for e in ((0,1),(0,2),(1,2)): m.add_element(Truss2D(e,210e9,1e-4))
for d in (0,1,3): m.constrain(d)
m.add_load(5,-10000)
r=StaticAnalysis(m).solve()
print("U =",r.solution)
print("R =",r.reaction)
