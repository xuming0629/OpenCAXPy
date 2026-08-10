from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from opencaxpy import HexahedronMesh, VTKMeshViewer, VTKMeshViewerOptions

mesh = HexahedronMesh.from_box((0, 2, 0, 1, 0, 1), nx=2, ny=1, nz=1)
print(mesh.summary())
print('volume =', mesh.entity_measure('cell'))

VTKMeshViewer(
    mesh,
    VTKMeshViewerOptions(
        show_surface=True,
        show_edges=True,
        show_nodes=True,
        show_cell_ids=True,
        title='Hexa8 Mesh',
    ),
).show()
