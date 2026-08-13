from __future__ import annotations

from .base import Plot
from ..options import MeshStyle


class MeshPlot(Plot):
    """网格可视化 Plot。"""

    def __init__(
        self,
        mesh,
        *,
        style: MeshStyle | None = None,
        title: str | None = None,
    ):
        self.mesh = mesh
        self.style = style or MeshStyle()
        self.title = title

    @property
    def backend(self) -> str:
        return "vtk"

    def render(self, context):
        return context.render_mesh(self)
