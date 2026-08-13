from __future__ import annotations

from dataclasses import dataclass, field

Color = tuple[float, float, float]


@dataclass(frozen=True)
class OpenCAXTheme:
    """OpenCAXPy 默认可视化主题。

    网格颜色保持 Visualization v1.x 的原有风格。
    """

    # 浅灰背景
    background: Color = (0.94, 0.94, 0.94)

    # 红色节点
    node_color: Color = (0.90, 0.20, 0.18)

    # 深蓝色边
    edge_color: Color = (0.12, 0.32, 0.58)

    # 浅蓝色面
    face_color: Color = (0.45, 0.68, 0.88)

    # 浅绿色单元/表面
    cell_color: Color = (0.55, 0.78, 0.58)
    surface_color: Color = (0.55, 0.78, 0.58)

    # 深灰文字
    text_color: Color = (0.15, 0.15, 0.15)

    # 未变形网格
    undeformed_color: Color = (0.35, 0.35, 0.35)


DEFAULT_THEME = OpenCAXTheme()


@dataclass
class MeshStyle:
    """网格绘制样式。

    只描述网格本身的显示方式，不保存 title/window_size 等 Figure 属性。
    """

    show_surface: bool = True
    show_edges: bool = True
    show_nodes: bool = True
    show_boundary_only: bool = False

    show_node_ids: bool = False
    show_edge_ids: bool = False
    show_face_ids: bool = False
    show_cell_ids: bool = False

    point_size: float = 8.0
    line_width: float = 1.5
    surface_opacity: float = 0.35

    theme: OpenCAXTheme = field(default_factory=lambda: DEFAULT_THEME)


@dataclass
class FieldStyle:
    """标量/向量场显示样式。"""

    show_scalar_bar: bool = True
    scalar_bar_labels: int = 5
    scalar_range: tuple[float, float] | None = None

    show_vectors: bool = False
    vector_scale: float = 1.0


@dataclass
class DeformationStyle:
    """结构变形显示样式。"""

    enabled: bool = False
    scale: float | str = "auto"
    show_undeformed: bool = True
    undeformed_opacity: float = 0.45
    undeformed_line_width: float = 1.0


@dataclass
class FigureOptions:
    """整个可视化窗口/Figure 的配置。"""

    window_size: tuple[int, int] = (1200, 800)
    figsize: tuple[float, float] = (12.0, 7.0)
    dpi: int = 180
    title: str | None = None
    theme: OpenCAXTheme = field(default_factory=lambda: DEFAULT_THEME)
