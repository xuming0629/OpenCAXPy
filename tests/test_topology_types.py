from opencaxpy import *
def test_independent_topology_types():
    assert isinstance(rectangle_triangle(0,1,0,1,1,1).topology,TriangleTopology)
    assert isinstance(rectangle_quad(0,1,0,1,1,1).topology,QuadrilateralTopology)
    assert isinstance(box_tetra(0,1,0,1,0,1,1,1,1).topology,TetrahedronTopology)
    assert isinstance(box_hexa(0,1,0,1,0,1,1,1,1).topology,HexahedronTopology)
