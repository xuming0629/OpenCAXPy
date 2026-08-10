import numpy as np
from .mesh import Mesh

class TriangleMesh(Mesh):
    def __init__(self, points, cells):
        super().__init__(points, cells, "triangle3")

    @classmethod
    def from_box(
        cls,
        box=(0.0,1.0,0.0,1.0),
        nx=1,
        ny=1,
    ):
        xmin,xmax,ymin,ymax = box
        xs = np.linspace(xmin,xmax,nx+1)
        ys = np.linspace(ymin,ymax,ny+1)

        points = np.array(
            [(x,y) for y in ys for x in xs],
            dtype=float,
        )

        def nid(i,j):
            return j*(nx+1)+i

        cells = []

        for j in range(ny):
            for i in range(nx):
                n0 = nid(i,j)
                n1 = nid(i+1,j)
                n2 = nid(i+1,j+1)
                n3 = nid(i,j+1)
                cells.append((n0,n1,n2))
                cells.append((n0,n2,n3))

        return cls(
            points,
            np.asarray(cells,dtype=int),
        )
