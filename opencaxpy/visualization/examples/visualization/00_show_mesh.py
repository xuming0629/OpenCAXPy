"""Test 1: single 2-D mesh visualization."""

from opencaxpy.visualization import MeshStyle, show_mesh
from demo_mesh import triangle_mesh


mesh = triangle_mesh()

style = MeshStyle(
    show_surface=True,
    show_edges=True,
    show_nodes=True,
    show_node_ids=True,
    show_cell_ids=True,
)

show_mesh(mesh, style=style, title="Triangle Mesh")
