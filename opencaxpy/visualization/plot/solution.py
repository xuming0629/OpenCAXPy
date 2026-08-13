from __future__ import annotations
from .base import Plot
from ..options import MeshStyle, FieldStyle, DeformationStyle


class SolutionPlot(Plot):
    def __init__(self, mesh, solution, *, field, component=None, deformation=None,
                 scale=1.0, mesh_style=None, field_style=None, deformation_style=None,
                 title=None):
        self.mesh = mesh
        self.solution = solution
        self.field = field
        self.component = component
        self.deformation = deformation
        self.scale = scale
        self.mesh_style = mesh_style or MeshStyle(show_nodes=False)
        self.field_style = field_style or FieldStyle()
        self.deformation_style = deformation_style or DeformationStyle(
            enabled=deformation is not None, scale=scale
        )
        self.title = title

    @property
    def backend(self): return "vtk"

    def render(self, context):
        return context.render_solution(self)
