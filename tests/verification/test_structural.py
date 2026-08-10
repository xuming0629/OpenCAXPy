import numpy as np
from opencaxpy import StructuralModel,Truss2D,EulerBernoulliBeam2D,StaticAnalysis

def test_truss():
    p=np.array([[0,0],[2,0],[1,1.5]],float); m=StructuralModel(p,2)
    for e in ((0,1),(0,2),(1,2)): m.add_element(Truss2D(e,210e9,1e-4))
    for d in (0,1,3): m.constrain(d)
    m.add_load(5,-10000)
    r=StaticAnalysis(m).solve()
    assert abs(r.solution[5]+0.0007258223092729081)<1e-12

def test_beam():
    L,P,E,A,I=2.0,1000.0,210e9,0.01,8.333333333e-6
    m=StructuralModel(np.array([[0,0],[L,0]],float),3)
    m.add_element(EulerBernoulliBeam2D((0,1),E,A,I))
    for d in (0,1,2): m.constrain(d)
    m.add_load(4,-P)
    r=StaticAnalysis(m).solve()
    assert abs(r.solution[4]+P*L**3/(3*E*I))<1e-12
