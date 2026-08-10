# from __future__ import annotations
# from dataclasses import dataclass


# @dataclass
# class VTKMeshViewerOptions:
#     show_surface: bool = True
#     show_edges: bool = True
#     show_nodes: bool = True
#     show_boundary_only: bool = False

#     show_node_ids: bool = False
#     show_edge_ids: bool = False
#     show_face_ids: bool = False
#     show_cell_ids: bool = False

#     point_size: float = 8.0
#     line_width: float = 1.5
#     surface_opacity: float = 0.35

#     background: tuple[float, float, float] = (0.12, 0.14, 0.18)
#     surface_color: tuple[float, float, float] = (0.72, 0.78, 0.88)
#     edge_color: tuple[float, float, float] = (0.08, 0.08, 0.10)
#     node_color: tuple[float, float, float] = (0.92, 0.36, 0.22)
#     text_color: tuple[float, float, float] = (0.95, 0.95, 0.95)

#     window_size: tuple[int, int] = (1100, 800)
#     title: str = 'OpenCAXPy VTK Mesh Viewer'


from dataclasses import dataclass


@dataclass
class VTKMeshViewerOptions:
    show_surface: bool = True
    show_edges: bool = True
    show_nodes: bool = True
    show_boundary_only: bool = False

    # ID 显示
    show_node_ids: bool = False
    show_edge_ids: bool = False
    show_face_ids: bool = False
    show_cell_ids: bool = False

    # 尺寸
    point_size: float = 8.0
    line_width: float = 1.5
    surface_opacity: float = 0.35

    # -----------------------------
    # 颜色
    # -----------------------------

    # 背景：浅白灰
    background: tuple[float, float, float] = (
        0.94,
        0.94,
        0.94,
    )

    # 节点：红色
    node_color: tuple[float, float, float] = (
        0.90,
        0.20,
        0.18,
    )

    # 边：深蓝色
    edge_color: tuple[float, float, float] = (
        0.12,
        0.32,
        0.58,
    )

    # 面：浅蓝色
    face_color: tuple[float, float, float] = (
        0.45,
        0.68,
        0.88,
    )

    # 单元：浅绿色
    cell_color: tuple[float, float, float] = (
        0.55,
        0.78,
        0.58,
    )

    # 保留兼容旧接口
    surface_color: tuple[float, float, float] = (
        0.55,
        0.78,
        0.58,
    )

    # 文字：深灰
    text_color: tuple[float, float, float] = (
        0.15,
        0.15,
        0.15,
    )

    window_size: tuple[int, int] = (1100, 800)

    title: str = "OpenCAXPy VTK Mesh Viewer"
