from __future__ import annotations

import numpy as np

from ...mesh import HexaMesh, QuadMesh, TetraMesh, TriangleMesh
from .base import MeshGenerator


def _validate_count(name: str, value: int) -> int:
    value = int(value)
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


class TriangleRectangleGenerator(MeshGenerator):
    name = "triangle_rectangle"

    def generate(
        self,
        *,
        x_min: float = 0.0,
        x_max: float = 1.0,
        y_min: float = 0.0,
        y_max: float = 1.0,
        nx: int = 1,
        ny: int = 1,
        diagonal: str = "alternating",
        backend="numpy",
        device=None,
    ) -> TriangleMesh:
        nx = _validate_count("nx", nx)
        ny = _validate_count("ny", ny)

        if diagonal not in {
            "left",
            "right",
            "alternating",
        }:
            raise ValueError(
                "diagonal must be left, right or alternating"
            )

        xs = np.linspace(
            x_min,
            x_max,
            nx + 1,
        )

        ys = np.linspace(
            y_min,
            y_max,
            ny + 1,
        )

        points = np.asarray(
            [
                [x, y]
                for y in ys
                for x in xs
            ],
            dtype=float,
        )

        def nid(i: int, j: int) -> int:
            return j * (nx + 1) + i

        cells = []

        for j in range(ny):
            for i in range(nx):
                # 四边形局部节点：
                #
                # v3 -------- v2
                #  |          |
                #  |          |
                # v0 -------- v1
                #
                v0 = nid(i, j)
                v1 = nid(i + 1, j)
                v2 = nid(i + 1, j + 1)
                v3 = nid(i, j + 1)

                use_right = (
                    diagonal == "right"
                    or (
                        diagonal == "alternating"
                        and (i + j) % 2 == 0
                    )
                )

                if use_right:
                    # 对角线：v0 -- v2
                    #
                    # 三角形 1：
                    #   直角点为 v1
                    #   v1 -> v2 -> v0 为逆时针
                    #
                    # 三角形 2：
                    #   直角点为 v3
                    #   v3 -> v0 -> v2 为逆时针
                    cells.extend(
                        [
                            [v1, v2, v0],
                            [v3, v0, v2],
                        ]
                    )

                else:
                    # 对角线：v1 -- v3
                    #
                    # 三角形 1：
                    #   直角点为 v0
                    #   v0 -> v1 -> v3 为逆时针
                    #
                    # 三角形 2：
                    #   直角点为 v2
                    #   v2 -> v3 -> v1 为逆时针
                    cells.extend(
                        [
                            [v0, v1, v3],
                            [v2, v3, v1],
                        ]
                    )

        return TriangleMesh(
            points,
            cells,
            backend=backend,
            device=device,
        )


class QuadRectangleGenerator(MeshGenerator):
    name = "quad_rectangle"

    def generate(
        self,
        *,
        x_min: float = 0.0,
        x_max: float = 1.0,
        y_min: float = 0.0,
        y_max: float = 1.0,
        nx: int = 1,
        ny: int = 1,
        backend="numpy",
        device=None,
    ) -> QuadMesh:
        nx = _validate_count("nx", nx)
        ny = _validate_count("ny", ny)
        xs = np.linspace(x_min, x_max, nx + 1)
        ys = np.linspace(y_min, y_max, ny + 1)
        points = np.asarray([[x, y] for y in ys for x in xs], dtype=float)

        def nid(i, j):
            return j * (nx + 1) + i

        cells = []
        for j in range(ny):
            for i in range(nx):
                cells.append([
                    nid(i, j),
                    nid(i + 1, j),
                    nid(i + 1, j + 1),
                    nid(i, j + 1),
                ])
        return QuadMesh(points, cells, backend=backend, device=device)


class HexaBoxGenerator(MeshGenerator):
    name = "hexa_box"

    def generate(
        self,
        *,
        x_min=0.0, x_max=1.0,
        y_min=0.0, y_max=1.0,
        z_min=0.0, z_max=1.0,
        nx=1, ny=1, nz=1,
        backend="numpy",
        device=None,
    ) -> HexaMesh:
        nx = _validate_count("nx", nx)
        ny = _validate_count("ny", ny)
        nz = _validate_count("nz", nz)
        xs = np.linspace(x_min, x_max, nx + 1)
        ys = np.linspace(y_min, y_max, ny + 1)
        zs = np.linspace(z_min, z_max, nz + 1)
        points = np.asarray(
            [[x, y, z] for z in zs for y in ys for x in xs],
            dtype=float,
        )

        def nid(i, j, k):
            return k * (ny + 1) * (nx + 1) + j * (nx + 1) + i

        cells = []
        for k in range(nz):
            for j in range(ny):
                for i in range(nx):
                    cells.append([
                        nid(i, j, k),
                        nid(i + 1, j, k),
                        nid(i + 1, j + 1, k),
                        nid(i, j + 1, k),
                        nid(i, j, k + 1),
                        nid(i + 1, j, k + 1),
                        nid(i + 1, j + 1, k + 1),
                        nid(i, j + 1, k + 1),
                    ])
        return HexaMesh(points, cells, backend=backend, device=device)


class TetraBoxGenerator(MeshGenerator):
    name = "tetra_box"

    def generate(self, **kwargs) -> TetraMesh:
        hexa = HexaBoxGenerator().generate(**kwargs)
        points = hexa.backend.to_numpy(hexa.points)
        hexes = hexa.backend.to_numpy(hexa.cells)

        # Six tetrahedra sharing the body diagonal v0-v6.
        pattern = (
            (0, 1, 2, 6),
            (0, 2, 3, 6),
            (0, 3, 7, 6),
            (0, 7, 4, 6),
            (0, 4, 5, 6),
            (0, 5, 1, 6),
        )
        cells = [
            [int(cell[i]) for i in tet]
            for cell in hexes
            for tet in pattern
        ]
        return TetraMesh(
            points,
            cells,
            backend=hexa.backend,
            device=hexa.device,
        )
