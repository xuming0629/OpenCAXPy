import numpy as np
from opencaxpy import StructuralModel,EulerBernoulliBeam2D,StaticAnalysis
L,P,E,A,I=2.0,1000.0,210e9,0.01,8.333333333e-6
m=StructuralModel(np.array([[0,0],[L,0]],float),3)
m.add_element(EulerBernoulliBeam2D((0,1),E,A,I))
for d in (0,1,2): m.constrain(d)
m.add_load(4,-P)
r=StaticAnalysis(m).solve()
print("uy =",r.solution[4])
print("theory =",-P*L**3/(3*E*I))
