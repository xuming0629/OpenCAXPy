from __future__ import annotations


class MeshGeometry:
    """Geometry operations isolated from topology construction."""

    def __init__(self, mesh) -> None:
        self.mesh = mesh

    @property
    def backend(self):
        return self.mesh.backend

    def barycenter(self, entity: str = "cell"):
        if entity == "node":
            return self.mesh.points

        connectivity = self.mesh.topology.connectivity(
            entity,
            "node",
        )
        rows = connectivity.to_lists()
        values = [
            self.backend.mean(
                self.mesh.points[
                    self.backend.asarray(
                        row,
                        dtype=self.backend.dtype_int(),
                        device=self.mesh.device,
                    )
                ],
                axis=0,
            )
            for row in rows
        ]

        return self.backend.stack(values, axis=0)

    def measure(self, entity: str = "cell"):
        if entity == "edge":
            edges = self.mesh.topology.entities("edge")
            vectors = (
                self.mesh.points[edges[:, 1]]
                - self.mesh.points[edges[:, 0]]
            )
            return self.backend.norm(vectors, axis=1)

        if entity != "cell":
            raise KeyError(
                "v1.0 geometry supports edge and cell measures"
            )

        family = self.mesh.cell_type.family

        if family == "triangle":
            return self._triangle_area()

        if family == "quad":
            return self._quad_area()

        if family == "tetra":
            return self._tetra_volume()

        if family == "hexa":
            return self._hexa_volume()

        raise NotImplementedError(
            f"cell measure is not implemented for {family}"
        )

    def _corner_points(self):
        corners = self.mesh.cell_type.corner_nodes
        return self.mesh.points[
            self.mesh.cells[:, corners]
        ]

    def _triangle_area(self):
        p = self._corner_points()
        ab = p[:, 1] - p[:, 0]
        ac = p[:, 2] - p[:, 0]

        if self.mesh.geometric_dimension == 2:
            value = ab[:, 0] * ac[:, 1] - ab[:, 1] * ac[:, 0]
            return 0.5 * self.backend.abs(value)

        return 0.5 * self.backend.norm(
            self.backend.cross(ab, ac),
            axis=1,
        )

    def _quad_area(self):
        p = self._corner_points()

        def tri(a, b, c):
            ab = b - a
            ac = c - a

            if self.mesh.geometric_dimension == 2:
                value = (
                    ab[:, 0] * ac[:, 1]
                    - ab[:, 1] * ac[:, 0]
                )
                return 0.5 * self.backend.abs(value)

            return 0.5 * self.backend.norm(
                self.backend.cross(ab, ac),
                axis=1,
            )

        return tri(p[:, 0], p[:, 1], p[:, 2]) + tri(
            p[:, 0], p[:, 2], p[:, 3]
        )

    def _tetra_volume(self):
        p = self._corner_points()
        a = p[:, 1] - p[:, 0]
        b = p[:, 2] - p[:, 0]
        c = p[:, 3] - p[:, 0]
        triple = self.backend.sum(
            self.backend.cross(a, b) * c,
            axis=1,
        )
        return self.backend.abs(triple) / 6.0

    def _hexa_volume(self):
        p = self._corner_points()
        decomposition = (
            (0, 1, 2, 6),
            (0, 2, 3, 6),
            (0, 3, 7, 6),
            (0, 7, 4, 6),
            (0, 4, 5, 6),
            (0, 5, 1, 6),
        )

        volumes = self.backend.zeros(
            (self.mesh.num_cells,),
            dtype=self.backend.dtype_float(),
            device=self.mesh.device,
        )

        for i, j, k, l in decomposition:
            a = p[:, j] - p[:, i]
            b = p[:, k] - p[:, i]
            c = p[:, l] - p[:, i]
            triple = self.backend.sum(
                self.backend.cross(a, b) * c,
                axis=1,
            )
            volumes = volumes + self.backend.abs(triple) / 6.0

        return volumes
