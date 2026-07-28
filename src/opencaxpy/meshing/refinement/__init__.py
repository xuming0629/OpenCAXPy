from .api import available_refinement_methods, refine
from .base import MeshRefiner
from .context import RefinementContext
from .hexahedron import HexaUniformRefiner
from .point_manager import EntityPointManager
from .quadrilateral import QuadUniformRefiner
from .registry import RefinementRegistry, refinement_registry
from .result import RefinementResult
from .tetrahedron import TetraUniformRefiner
from .transfer import RefinementDataTransfer
from .triangle import (
    TriangleLongestEdgeRefiner,
    TriangleNewestVertexRefiner,
    TriangleUniformRefiner,
)

for _refiner in (
    TriangleUniformRefiner(),
    TriangleLongestEdgeRefiner(),
    TriangleNewestVertexRefiner(),
    QuadUniformRefiner(),
    TetraUniformRefiner(),
    HexaUniformRefiner(),
):
    key = (_refiner.supported_cell_types[0], _refiner.method)
    if key not in refinement_registry.entries():
        refinement_registry.register(_refiner)

__all__ = [
    "refine",
    "available_refinement_methods",
    "MeshRefiner",
    "RefinementContext",
    "RefinementResult",
    "RefinementRegistry",
    "refinement_registry",
    "EntityPointManager",
    "RefinementDataTransfer",
    "TriangleUniformRefiner",
    "TriangleLongestEdgeRefiner",
    "TriangleNewestVertexRefiner",
    "QuadUniformRefiner",
    "TetraUniformRefiner",
    "HexaUniformRefiner",
]
