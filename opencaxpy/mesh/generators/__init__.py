"""OpenCAXPy 内置规则网格生成器。"""

from .interval import generate_interval
from .box2d import generate_quad_box, generate_triangle_box
from .box3d import generate_hexa_box, generate_tetra_box

__all__ = [
    "generate_interval",
    "generate_triangle_box",
    "generate_quad_box",
    "generate_tetra_box",
    "generate_hexa_box",
]
