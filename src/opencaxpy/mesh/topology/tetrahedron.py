from .base import BaseTopology
class TetrahedronTopology(BaseTopology):
    local_edges=((0,1),(1,2),(2,0),(0,3),(1,3),(2,3))
    local_faces=((0,2,1),(0,1,3),(1,2,3),(2,0,3))
