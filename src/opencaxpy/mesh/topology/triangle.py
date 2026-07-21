from .base import BaseTopology
class TriangleTopology(BaseTopology):
    local_edges=((0,1),(1,2),(2,0))
