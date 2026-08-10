import vtk
from opencaxpy import (
    TriangleMesh,
    HexahedronMesh,
    to_vtk_unstructured_grid,
)


def test_triangle_to_vtk():
    mesh = TriangleMesh.from_box((0,1,0,1), 1, 1)
    grid = to_vtk_unstructured_grid(mesh)
    assert isinstance(grid, vtk.vtkUnstructuredGrid)
    assert grid.GetNumberOfPoints() == 4
    assert grid.GetNumberOfCells() == 2
    assert grid.GetCellType(0) == vtk.VTK_TRIANGLE


def test_hexa_to_vtk():
    mesh = HexahedronMesh.from_box((0,1,0,1,0,1), 1, 1, 1)
    grid = to_vtk_unstructured_grid(mesh)
    assert grid.GetNumberOfPoints() == 8
    assert grid.GetNumberOfCells() == 1
    assert grid.GetCellType(0) == vtk.VTK_HEXAHEDRON
