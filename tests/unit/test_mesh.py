from opencaxpy import TriangleMesh
def test_area():
    m=TriangleMesh.from_box((0,1,0,1),4,4)
    assert abs(m.entity_measure().sum()-1.0)<1e-12
