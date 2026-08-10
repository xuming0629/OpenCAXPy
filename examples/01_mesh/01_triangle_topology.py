from opencaxpy import TriangleMesh, VTKMeshViewer, VTKMeshViewerOptions
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


mesh = TriangleMesh.from_box((0, 1, 0, 1), nx=2, ny=2)
print(mesh.summary())
print('cell_to_edge =\n', mesh.cell_to_edge())
print('boundary edges =', mesh.boundary_edge_index())

viewer = VTKMeshViewer(
    mesh,
    VTKMeshViewerOptions(
        show_surface=True,
        show_edges=True,
        show_nodes=True,
        show_node_ids=True,
        show_cell_ids=True,
        show_edge_ids=True,
        title='Triangle3 Mesh',
    ),
)
viewer.show()
