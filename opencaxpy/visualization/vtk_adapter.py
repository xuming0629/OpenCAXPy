from __future__ import annotations

import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk


VTK_CELL_TYPES = {
    'line2': vtk.VTK_LINE,
    'triangle3': vtk.VTK_TRIANGLE,
    'quad4': vtk.VTK_QUAD,
    'tetra4': vtk.VTK_TETRA,
    'hexa8': vtk.VTK_HEXAHEDRON,
}


def _points_3d(points):
    points = np.asarray(points, dtype=float)
    if points.shape[1] == 3:
        return points
    if points.shape[1] == 2:
        return np.column_stack([points, np.zeros(len(points))])
    if points.shape[1] == 1:
        return np.column_stack([points[:, 0], np.zeros((len(points), 2))])
    raise ValueError('VTK adapter supports geometric dimension 1, 2, or 3')


def to_vtk_unstructured_grid(mesh, *, point_data=None, cell_data=None):
    """Convert an OpenCAXPy Mesh into vtkUnstructuredGrid.

    This function is the single mesh-to-VTK bridge used by viewers and future
    result visualization, so solver/physics code never needs to import VTK.
    """
    if mesh.cell_type not in VTK_CELL_TYPES:
        raise NotImplementedError(f'VTK mapping missing for {mesh.cell_type!r}')

    vtk_points = vtk.vtkPoints()
    xyz = _points_3d(mesh.points)
    vtk_points.SetData(numpy_to_vtk(xyz, deep=True))

    grid = vtk.vtkUnstructuredGrid()
    grid.SetPoints(vtk_points)

    vtk_type = VTK_CELL_TYPES[mesh.cell_type]
    for cell in mesh.cells:
        ids = vtk.vtkIdList()
        for node_id in cell:
            ids.InsertNextId(int(node_id))
        grid.InsertNextCell(vtk_type, ids)

    if point_data:
        for name, values in point_data.items():
            arr = np.asarray(values)
            vtk_arr = numpy_to_vtk(arr, deep=True)
            vtk_arr.SetName(str(name))
            grid.GetPointData().AddArray(vtk_arr)

    if cell_data:
        for name, values in cell_data.items():
            arr = np.asarray(values)
            vtk_arr = numpy_to_vtk(arr, deep=True)
            vtk_arr.SetName(str(name))
            grid.GetCellData().AddArray(vtk_arr)

    return grid


def make_polydata_from_entities(mesh, entity_type, indices=None):
    """Create VTK polydata for mesh edges/faces without duplicating Mesh logic."""
    entities = mesh.entity(entity_type)
    if indices is not None:
        entities = entities[np.asarray(indices, dtype=int)]

    xyz = _points_3d(mesh.points)
    vtk_points = vtk.vtkPoints()
    vtk_points.SetData(numpy_to_vtk(xyz, deep=True))

    poly = vtk.vtkPolyData()
    poly.SetPoints(vtk_points)

    if entity_type == 'edge':
        cells = vtk.vtkCellArray()
        for edge in entities:
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, int(edge[0]))
            line.GetPointIds().SetId(1, int(edge[1]))
            cells.InsertNextCell(line)
        poly.SetLines(cells)
        return poly

    if entity_type == 'face':
        cells = vtk.vtkCellArray()
        for face in entities:
            polygon = vtk.vtkPolygon()
            polygon.GetPointIds().SetNumberOfIds(len(face))
            for i, node_id in enumerate(face):
                polygon.GetPointIds().SetId(i, int(node_id))
            cells.InsertNextCell(polygon)
        poly.SetPolys(cells)
        return poly

    raise ValueError(f'Unsupported entity_type={entity_type!r}')


def make_point_cloud(points):
    xyz = _points_3d(points)
    vtk_points = vtk.vtkPoints()
    vtk_points.SetData(numpy_to_vtk(xyz, deep=True))

    poly = vtk.vtkPolyData()
    poly.SetPoints(vtk_points)

    glyph = vtk.vtkVertexGlyphFilter()
    glyph.SetInputData(poly)
    glyph.Update()
    return glyph.GetOutput()
