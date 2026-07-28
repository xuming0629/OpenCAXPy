from __future__ import annotations

from .registry import mesh_generator_registry


class MeshFactory:
    @staticmethod
    def create(name: str, **kwargs):
        return mesh_generator_registry.create(name, **kwargs)

    @staticmethod
    def available() -> tuple[str, ...]:
        return mesh_generator_registry.names()

    @staticmethod
    def triangle_rectangle(*args, **kwargs):
        keys = ("x_min", "x_max", "y_min", "y_max", "nx", "ny")
        if args:
            kwargs = {**dict(zip(keys, args)), **kwargs}
        return MeshFactory.create("triangle_rectangle", **kwargs)

    @staticmethod
    def quad_rectangle(*args, **kwargs):
        keys = ("x_min", "x_max", "y_min", "y_max", "nx", "ny")
        if args:
            kwargs = {**dict(zip(keys, args)), **kwargs}
        return MeshFactory.create("quad_rectangle", **kwargs)

    @staticmethod
    def tetra_box(*args, **kwargs):
        keys = (
            "x_min", "x_max", "y_min", "y_max",
            "z_min", "z_max", "nx", "ny", "nz",
        )
        if args:
            kwargs = {**dict(zip(keys, args)), **kwargs}
        return MeshFactory.create("tetra_box", **kwargs)

    @staticmethod
    def hexa_box(*args, **kwargs):
        keys = (
            "x_min", "x_max", "y_min", "y_max",
            "z_min", "z_max", "nx", "ny", "nz",
        )
        if args:
            kwargs = {**dict(zip(keys, args)), **kwargs}
        return MeshFactory.create("hexa_box", **kwargs)
