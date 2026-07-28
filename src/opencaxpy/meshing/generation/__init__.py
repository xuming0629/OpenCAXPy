from .base import MeshGenerator
from .factory import MeshFactory
from .registry import MeshGeneratorRegistry, mesh_generator_registry
from .structured import (
    HexaBoxGenerator,
    QuadRectangleGenerator,
    TetraBoxGenerator,
    TriangleRectangleGenerator,
)

for _generator in (
    TriangleRectangleGenerator(),
    QuadRectangleGenerator(),
    TetraBoxGenerator(),
    HexaBoxGenerator(),
):
    if _generator.name not in mesh_generator_registry.names():
        mesh_generator_registry.register(_generator)

__all__ = [
    "MeshGenerator",
    "MeshGeneratorRegistry",
    "mesh_generator_registry",
    "MeshFactory",
    "TriangleRectangleGenerator",
    "QuadRectangleGenerator",
    "TetraBoxGenerator",
    "HexaBoxGenerator",
]
