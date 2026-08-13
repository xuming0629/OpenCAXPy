"""OpenCAXPy Visualization v2.0 public API."""

from .api import (
    show,
    show_mesh,
    show_solution,
    show_convergence,
    view_mesh,
)
from .figure import Figure
from .field import Field
from .solution import Solution
from .options import (
    OpenCAXTheme,
    DEFAULT_THEME,
    MeshStyle,
    FieldStyle,
    DeformationStyle,
    FigureOptions,
)
from .plot.mesh import MeshPlot
from .plot.solution import SolutionPlot
from .plot.convergence import (
    ConvergencePlot,
    ConvergenceResult,
    estimate_convergence_order,
)

__version__ = "2.0.0"

__all__ = [
    # High-level API
    "show",
    "show_mesh",
    "show_solution",
    "show_convergence",
    "view_mesh",

    # Figure / plot
    "Figure",
    "MeshPlot",
    "SolutionPlot",
    "ConvergencePlot",

    # Result data model
    "Field",
    "Solution",

    # Convergence
    "ConvergenceResult",
    "estimate_convergence_order",

    # Styles
    "OpenCAXTheme",
    "DEFAULT_THEME",
    "MeshStyle",
    "FieldStyle",
    "DeformationStyle",
    "FigureOptions",
]
