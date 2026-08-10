from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from opencaxpy import QuadrangleMesh, VTKMeshViewer, VTKMeshViewerOptions

mesh = QuadrangleMesh.from_box((0, 3, 0, 2), nx=3, ny=2)
print(mesh.summary())
print('quality =', mesh.cell_quality())

VTKMeshViewer(
    mesh,
    VTKMeshViewerOptions(
        show_surface=True,
        show_edges=True,
        show_nodes=True,
        show_cell_ids=True,
        title='Quad4 Mesh',
    ),
).show()
