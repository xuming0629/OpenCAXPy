from __future__ import annotations

import numpy as np

from .cell_type import CellType
from .mesh import Mesh


def rectangle_quad(
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    nx: int,
    ny: int,
    *,
    backend: str = "numpy",
    device: str | None = None,
) -> Mesh:
    if nx <= 0 or ny <= 0:
        raise ValueError("nx and ny must be positive")
    if not (xmax > xmin and ymax > ymin):
        raise ValueError("rectangle bounds must be increasing")

    xs = np.linspace(xmin, xmax, nx + 1)
    ys = np.linspace(ymin, ymax, ny + 1)
    xx, yy = np.meshgrid(xs, ys, indexing="xy")
    points = np.column_stack((xx.ravel(), yy.ravel()))

    def node(i, j):
        return j * (nx + 1) + i

    cells = []
    for j in range(ny):
        for i in range(nx):
            n0 = node(i, j)
            n1 = node(i + 1, j)
            n2 = node(i + 1, j + 1)
            n3 = node(i, j + 1)
            cells.append((n0, n1, n2, n3))

    return Mesh(
        points,
        np.asarray(cells, dtype=np.int64),
        CellType.QUAD4,
        backend_name=backend,
        device_hint=device,
    )


def rectangle_triangle(
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    nx: int,
    ny: int,
    *,
    diagonal: str = "alternating",
    backend: str = "numpy",
    device: str | None = None,
) -> Mesh:
    quad = rectangle_quad(
        xmin, xmax, ymin, ymax, nx, ny,
        backend="numpy",
        device="cpu",
    )
    quads = quad.cells
    triangles = []

    for cell_id, (n0, n1, n2, n3) in enumerate(quads):
        if diagonal == "right":
            use_right = True
        elif diagonal == "left":
            use_right = False
        elif diagonal == "alternating":
            i = cell_id % nx
            j = cell_id // nx
            use_right = ((i + j) % 2) == 0
        else:
            raise ValueError("diagonal must be 'right', 'left' or 'alternating'")

        if use_right:
            triangles.extend(((n0, n1, n2), (n0, n2, n3)))
        else:
            triangles.extend(((n0, n1, n3), (n1, n2, n3)))

    return Mesh(
        quad.points,
        np.asarray(triangles, dtype=np.int64),
        CellType.TRIANGLE3,
        backend_name=backend,
        device_hint=device,
    )


def box_hexa(
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    zmin: float,
    zmax: float,
    nx: int,
    ny: int,
    nz: int,
    *,
    backend: str = "numpy",
    device: str | None = None,
) -> Mesh:
    if nx <= 0 or ny <= 0 or nz <= 0:
        raise ValueError("nx, ny and nz must be positive")
    if not (xmax > xmin and ymax > ymin and zmax > zmin):
        raise ValueError("box bounds must be increasing")

    xs = np.linspace(xmin, xmax, nx + 1)
    ys = np.linspace(ymin, ymax, ny + 1)
    zs = np.linspace(zmin, zmax, nz + 1)
    xx, yy, zz = np.meshgrid(xs, ys, zs, indexing="xy")
    points = np.column_stack((xx.ravel(), yy.ravel(), zz.ravel()))

    def node(i, j, k):
        return k + (nz + 1) * (i + (nx + 1) * j)

    cells = []
    for j in range(ny):
        for i in range(nx):
            for k in range(nz):
                n0 = node(i, j, k)
                n1 = node(i + 1, j, k)
                n2 = node(i + 1, j + 1, k)
                n3 = node(i, j + 1, k)
                n4 = node(i, j, k + 1)
                n5 = node(i + 1, j, k + 1)
                n6 = node(i + 1, j + 1, k + 1)
                n7 = node(i, j + 1, k + 1)
                cells.append((n0, n1, n2, n3, n4, n5, n6, n7))

    return Mesh(
        points,
        np.asarray(cells, dtype=np.int64),
        CellType.HEXA8,
        backend_name=backend,
        device_hint=device,
    )


def box_tetra(
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    zmin: float,
    zmax: float,
    nx: int,
    ny: int,
    nz: int,
    *,
    backend: str = "numpy",
    device: str | None = None,
) -> Mesh:
    hexa = box_hexa(
        xmin, xmax, ymin, ymax, zmin, zmax,
        nx, ny, nz,
        backend="numpy",
        device="cpu",
    )
    # A consistent six-tetra decomposition around body diagonal 0-6.
    local_tets = np.asarray([
        [0, 1, 2, 6],
        [0, 2, 3, 6],
        [0, 3, 7, 6],
        [0, 7, 4, 6],
        [0, 4, 5, 6],
        [0, 5, 1, 6],
    ], dtype=np.int64)
    cells = hexa.cells[:, local_tets].reshape(-1, 4)

    return Mesh(
        hexa.points,
        cells,
        CellType.TETRA4,
        backend_name=backend,
        device_hint=device,
    )
