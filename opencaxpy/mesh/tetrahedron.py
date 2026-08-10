import numpy as np
from .mesh import Mesh

class TetrahedronMesh(Mesh):
    def __init__(self, points, cells):
        super().__init__(points, cells, "tetra4")

    @classmethod
    def unit_tetrahedron(cls):
        return cls(
            np.array([
                [0.,0.,0.],
                [1.,0.,0.],
                [0.,1.,0.],
                [0.,0.,1.],
            ]),
            np.array([[0,1,2,3]],dtype=int),
        )

    @classmethod
    def from_box(cls):
        points = np.array([
            [0,0,0],[1,0,0],[1,1,0],[0,1,0],
            [0,0,1],[1,0,1],[1,1,1],[0,1,1],
        ],dtype=float)

        cells = np.array([
            [0,1,2,6],
            [0,2,3,6],
            [0,3,7,6],
            [0,7,4,6],
            [0,4,5,6],
            [0,5,1,6],
        ],dtype=int)

        return cls(points,cells)
