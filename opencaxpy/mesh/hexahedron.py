import numpy as np
from .mesh import Mesh

class HexahedronMesh(Mesh):
    def __init__(self, points, cells):
        super().__init__(points, cells, "hexa8")

    @classmethod
    def from_box(
        cls,
        box=(0,1,0,1,0,1),
        nx=1,
        ny=1,
        nz=1,
    ):
        xmin,xmax,ymin,ymax,zmin,zmax = box

        xs = np.linspace(xmin,xmax,nx+1)
        ys = np.linspace(ymin,ymax,ny+1)
        zs = np.linspace(zmin,zmax,nz+1)

        points = np.array([
            (x,y,z)
            for z in zs
            for y in ys
            for x in xs
        ],dtype=float)

        def nid(i,j,k):
            return (
                k*(ny+1)*(nx+1)
                + j*(nx+1)
                + i
            )

        cells = []

        for k in range(nz):
            for j in range(ny):
                for i in range(nx):
                    cells.append((
                        nid(i,j,k),
                        nid(i+1,j,k),
                        nid(i+1,j+1,k),
                        nid(i,j+1,k),
                        nid(i,j,k+1),
                        nid(i+1,j,k+1),
                        nid(i+1,j+1,k+1),
                        nid(i,j+1,k+1),
                    ))

        return cls(
            points,
            np.asarray(cells,dtype=int),
        )
