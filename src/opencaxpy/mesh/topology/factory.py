from ..cell_type import CellType
from .triangle import TriangleTopology
from .quadrilateral import QuadrilateralTopology
from .tetrahedron import TetrahedronTopology
from .hexahedron import HexahedronTopology
_MAP={CellType.TRIANGLE3:TriangleTopology,CellType.TRIANGLE6:TriangleTopology,CellType.QUAD4:QuadrilateralTopology,CellType.QUAD8:QuadrilateralTopology,CellType.QUAD9:QuadrilateralTopology,CellType.TETRA4:TetrahedronTopology,CellType.TETRA10:TetrahedronTopology,CellType.HEXA8:HexahedronTopology,CellType.HEXA20:HexahedronTopology,CellType.HEXA27:HexahedronTopology}
def create_topology(mesh):
    try: return _MAP[mesh.cell_type](mesh)
    except KeyError as exc: raise NotImplementedError(f'No topology implementation for {mesh.cell_type.value}') from exc
