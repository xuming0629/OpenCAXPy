from __future__ import annotations
import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk

VTK_CELL_TYPES = {
    "line2": vtk.VTK_LINE,
    "line3": vtk.VTK_QUADRATIC_EDGE,
    "triangle3": vtk.VTK_TRIANGLE,
    "triangle6": vtk.VTK_QUADRATIC_TRIANGLE,
    "quad4": vtk.VTK_QUAD,
    "quad8": vtk.VTK_QUADRATIC_QUAD,
    "quad9": vtk.VTK_BIQUADRATIC_QUAD,
    "tetra4": vtk.VTK_TETRA,
    "hexa8": vtk.VTK_HEXAHEDRON,
    "wedge6": vtk.VTK_WEDGE,
    "pyramid5": vtk.VTK_PYRAMID,
}


def points_3d(points):
    p = np.asarray(points, dtype=float)
    if p.ndim != 2:
        raise ValueError("points must be a 2-D array")
    if p.shape[1] == 3: return p
    if p.shape[1] == 2: return np.column_stack([p, np.zeros(len(p))])
    if p.shape[1] == 1: return np.column_stack([p[:, 0], np.zeros((len(p), 2))])
    raise ValueError("geometric dimension must be 1, 2 or 3")


def _cell_type_name(mesh):
    ct = mesh.cell_type
    return ct.name if hasattr(ct, "name") else str(ct)


def to_vtk_unstructured_grid(mesh, *, point_data=None, cell_data=None):
    """The single OpenCAXPy Mesh -> VTK bridge."""
    name = _cell_type_name(mesh)
    if name not in VTK_CELL_TYPES:
        raise NotImplementedError(f"VTK mapping missing for {name!r}")
    pts = vtk.vtkPoints(); pts.SetData(numpy_to_vtk(points_3d(mesh.points), deep=True))
    grid = vtk.vtkUnstructuredGrid(); grid.SetPoints(pts)
    for cell in np.asarray(mesh.cells):
        ids = vtk.vtkIdList()
        for i in cell: ids.InsertNextId(int(i))
        grid.InsertNextCell(VTK_CELL_TYPES[name], ids)
    _attach_data(grid.GetPointData(), point_data, grid.GetNumberOfPoints(), "point")
    _attach_data(grid.GetCellData(), cell_data, grid.GetNumberOfCells(), "cell")
    return grid


def _attach_data(target, mapping, expected, association):
    if not mapping: return
    for name, values in mapping.items():
        arr = np.asarray(values, dtype=float)
        if arr.ndim == 0 or len(arr) != expected:
            raise ValueError(f"{association} data {name!r}: expected {expected} rows")
        va = numpy_to_vtk(np.ascontiguousarray(arr), deep=True, array_type=vtk.VTK_DOUBLE)
        va.SetName(str(name)); target.AddArray(va)
