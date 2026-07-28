from __future__ import annotations

from dataclasses import dataclass


Color = tuple[float, float, float]


def _validate_color(name: str, value: Color) -> None:
    if len(value) != 3:
        raise ValueError(f"{name} must contain exactly three components")
    if any(component < 0.0 or component > 1.0 for component in value):
        raise ValueError(f"{name} components must be in [0.0, 1.0]")


@dataclass(slots=True)
class PlotOptions:
    # Visibility
    show_nodes: bool = False
    show_edges: bool = True
    show_boundary: bool = False
    show_node_ids: bool = False
    show_cell_ids: bool = False
    show_edge_ids: bool = False

    # Scalar field
    scalar_name: str | None = None
    scalar_location: str = "cell"
    cmap: str = "viridis"
    show_scalar_bar: bool = True

    # Geometry colors
    surface_color: Color = (0.82, 0.86, 0.92)
    node_color: Color = (0.90, 0.25, 0.18)
    edge_color: Color = (0.15, 0.15, 0.18)
    boundary_color: Color = (0.95, 0.45, 0.08)

    # Label colors
    node_label_color: Color = (0.95, 0.20, 0.15)
    edge_label_color: Color = (0.10, 0.45, 0.95)
    cell_label_color: Color = (0.10, 0.70, 0.25)

    # Label font sizes
    node_label_font_size: int = 10
    edge_label_font_size: int = 10
    cell_label_font_size: int = 10

    # Geometry sizes
    edge_width: float = 1.0
    boundary_width: float = 2.5
    node_size: float = 18.0

    # Canvas
    background_color: Color = (1.0, 1.0, 1.0)
    title: str | None = None
    equal_aspect: bool = True
    show: bool = True

    def __post_init__(self) -> None:
        for name in (
            "surface_color",
            "node_color",
            "edge_color",
            "boundary_color",
            "node_label_color",
            "edge_label_color",
            "cell_label_color",
            "background_color",
        ):
            _validate_color(name, getattr(self, name))

        if self.scalar_location not in {"point", "cell"}:
            raise ValueError("scalar_location must be 'point' or 'cell'")

        if self.edge_width <= 0.0:
            raise ValueError("edge_width must be positive")
        if self.boundary_width <= 0.0:
            raise ValueError("boundary_width must be positive")
        if self.node_size <= 0.0:
            raise ValueError("node_size must be positive")


@dataclass(slots=True)
class ViewerOptions:
    # Visibility
    show_nodes: bool = False
    show_edges: bool = True
    show_boundary: bool = False
    show_node_ids: bool = False
    show_edge_ids: bool = False
    show_cell_ids: bool = False

    # Scalar field
    scalar_name: str | None = None
    scalar_location: str = "cell"
    show_scalar_bar: bool = True

    # Geometry colors
    surface_color: Color = (0.82, 0.86, 0.92)
    node_color: Color = (0.90, 0.25, 0.18)
    edge_color: Color = (0.15, 0.15, 0.18)
    boundary_color: Color = (0.95, 0.45, 0.08)

    # Label colors
    node_label_color: Color = (0.95, 0.20, 0.15)
    edge_label_color: Color = (0.10, 0.45, 0.95)
    cell_label_color: Color = (0.10, 0.70, 0.25)

    # Label font sizes
    node_label_font_size: int = 14
    edge_label_font_size: int = 14
    cell_label_font_size: int = 14

    # Geometry sizes
    node_size: float = 7.0
    edge_width: float = 1.0
    boundary_width: float = 3.0

    # Renderer
    background_color: Color = (0.08, 0.10, 0.14)
    window_size: tuple[int, int] = (1000, 800)
    title: str = "OpenCAXPy Viewer"

    def __post_init__(self) -> None:
        for name in (
            "surface_color",
            "node_color",
            "edge_color",
            "boundary_color",
            "node_label_color",
            "edge_label_color",
            "cell_label_color",
            "background_color",
        ):
            _validate_color(name, getattr(self, name))

        if self.scalar_location not in {"point", "cell"}:
            raise ValueError("scalar_location must be 'point' or 'cell'")

        if len(self.window_size) != 2:
            raise ValueError("window_size must contain width and height")

        if self.node_size <= 0.0:
            raise ValueError("node_size must be positive")
        if self.edge_width <= 0.0:
            raise ValueError("edge_width must be positive")
        if self.boundary_width <= 0.0:
            raise ValueError("boundary_width must be positive")
