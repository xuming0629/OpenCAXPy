"""Test 2: multiple meshes in one row."""

from opencaxpy.visualization import show_mesh
from demo_mesh import coarse_triangle_mesh, triangle_mesh


show_mesh(
    [coarse_triangle_mesh(), triangle_mesh()],
    title="Mesh",
    layout=(1, 2),
)
