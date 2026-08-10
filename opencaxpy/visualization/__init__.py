from .options import VTKMeshViewerOptions
from .vtk_adapter import to_vtk_unstructured_grid
from .vtk_mesh_viewer import VTKMeshViewer, view_mesh

# Compatibility alias for code written against early v1.1.
MeshViewerOptions = VTKMeshViewerOptions
MeshViewer = VTKMeshViewer

__all__ = [
    'VTKMeshViewerOptions',
    'VTKMeshViewer',
    'to_vtk_unstructured_grid',
    'view_mesh',
    'MeshViewerOptions',
    'MeshViewer',
]
