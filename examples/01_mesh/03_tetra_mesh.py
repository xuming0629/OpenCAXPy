from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from opencaxpy import TetrahedronMesh, VTKMeshViewer, VTKMeshViewerOptions

mesh = TetrahedronMesh.from_box()
print(mesh.summary())
print('cell_to_face =\n', mesh.cell_to_face())
print('boundary faces =', mesh.boundary_face_index())

VTKMeshViewer(
    mesh,
    VTKMeshViewerOptions(
        show_surface=True,
        show_edges=True,
        show_nodes=True,
        show_boundary_only=False,
        show_cell_ids=True,
        title='Tetra4 Mesh',
    ),
).show()
