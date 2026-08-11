__version__ = "1.1.0"

from .backend import backend_manager
from .mesh import (
    Mesh,
    create_mesh,
    IntervalMesh,
    TriangleMesh,
    QuadrangleMesh,
    TetrahedronMesh,
    HexahedronMesh,
)
from .fields import Field
from .functionspace import DofEntity, LagrangeSpace, MixedSpace
from .discretization.fem import (
    BilinearForm,
    LinearForm,
    DiffusionIntegrator,
    SourceIntegrator,
    Truss2D,
    EulerBernoulliBeam2D,
    TimoshenkoBeam2D,
)
from .materials import (
    Material,
    MechanicalProperties,
    ThermalProperties,
    FluidProperties,
    ElectromagneticProperties,
)
from .sections import TrussSection, BeamSection
from .physics import PoissonPhysics, StructuralPhysics, HeatPhysics
from .models import Model, Problem, StructuralModel
from .boundary import DirichletBC
from .assembly import DenseAssembler
from .solvers import DenseDirectSolver
from .analysis import SteadyAnalysis, StaticAnalysis
from .results import Result, FieldResult
from .post import von_mises_3d

from .visualization import VTKMeshViewerOptions, VTKMeshViewer, to_vtk_unstructured_grid, view_mesh
