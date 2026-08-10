from __future__ import annotations

from pathlib import Path
import numpy as np
import vtk

from .options import VTKMeshViewerOptions
from .vtk_adapter import (
    make_point_cloud,
    make_polydata_from_entities,
    to_vtk_unstructured_grid,
)


class VTKMeshViewer:
    """VTK-native mesh viewer for OpenCAXPy.

    The mesh kernel has no dependency on VTK.  Only this visualization package
    performs the conversion to vtkUnstructuredGrid / vtkPolyData.
    """

    def __init__(self, mesh, options=None):
        self.mesh = mesh
        self.options = options or VTKMeshViewerOptions()

        self.renderer = vtk.vtkRenderer()
        self.window = vtk.vtkRenderWindow()
        self.window.SetWindowName(self.options.title)
        self.window.SetSize(*self.options.window_size)
        self.window.AddRenderer(self.renderer)

        self.interactor = vtk.vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.window)
        style = vtk.vtkInteractorStyleTrackballCamera()
        self.interactor.SetInteractorStyle(style)

        self._build_scene()

    def _build_scene(self):
        o = self.options
        self.renderer.SetBackground(*o.background)

        grid = to_vtk_unstructured_grid(self.mesh)

        if o.show_surface:
            if o.show_boundary_only and self.mesh.topological_dimension == 3:
                mapper = vtk.vtkPolyDataMapper()
                poly = make_polydata_from_entities(
                    self.mesh,
                    'face',
                    self.mesh.boundary_face_index(),
                )
                mapper.SetInputData(poly)
            else:
                mapper = vtk.vtkDataSetMapper()
                mapper.SetInputData(grid)

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(*o.surface_color)
            actor.GetProperty().SetOpacity(o.surface_opacity)
            self.renderer.AddActor(actor)

        if o.show_edges:
            edge_ids = None
            if o.show_boundary_only:
                edge_ids = self.mesh.boundary_edge_index()

            edge_poly = make_polydata_from_entities(
                self.mesh,
                'edge',
                edge_ids,
            )
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(edge_poly)
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(*o.edge_color)
            actor.GetProperty().SetLineWidth(o.line_width)
            self.renderer.AddActor(actor)

        if o.show_nodes:
            nodes = self.mesh.points
            if o.show_boundary_only:
                nodes = self.mesh.points[self.mesh.boundary_node_index()]

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(make_point_cloud(nodes))
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(*o.node_color)
            actor.GetProperty().SetPointSize(o.point_size)
            self.renderer.AddActor(actor)

        if o.show_node_ids:
            self._add_labels(
                self.mesh.points,
                [f'N{i}' for i in range(self.mesh.number_of_nodes())],
            )

        if o.show_edge_ids:
            centers = self.mesh.entity_barycenter('edge')
            self._add_labels(
                centers,
                [f'E{i}' for i in range(self.mesh.number_of_edges())],
            )

        if o.show_face_ids and self.mesh.topological_dimension == 3:
            centers = self.mesh.entity_barycenter('face')
            self._add_labels(
                centers,
                [f'F{i}' for i in range(self.mesh.number_of_faces())],
            )

        if o.show_cell_ids:
            centers = self.mesh.entity_barycenter('cell')
            self._add_labels(
                centers,
                [f'C{i}' for i in range(self.mesh.number_of_cells())],
            )

        axes = vtk.vtkAxesActor()
        widget = vtk.vtkOrientationMarkerWidget()
        widget.SetOrientationMarker(axes)
        widget.SetInteractor(self.interactor)
        widget.SetViewport(0.0, 0.0, 0.18, 0.18)
        widget.SetEnabled(1)
        widget.InteractiveOff()
        self._orientation_widget = widget

        self.renderer.ResetCamera()

    def _add_labels(self, points, labels):
        points = np.asarray(points, dtype=float)
        if points.shape[1] == 1:
            points = np.column_stack([points[:,0], np.zeros((len(points),2))])
        elif points.shape[1] == 2:
            points = np.column_stack([points, np.zeros(len(points))])

        vtk_points = vtk.vtkPoints()
        for p in points:
            vtk_points.InsertNextPoint(float(p[0]), float(p[1]), float(p[2]))

        poly = vtk.vtkPolyData()
        poly.SetPoints(vtk_points)

        label_array = vtk.vtkStringArray()
        label_array.SetName('labels')
        for label in labels:
            label_array.InsertNextValue(str(label))
        poly.GetPointData().AddArray(label_array)

        mapper = vtk.vtkLabeledDataMapper()
        mapper.SetInputData(poly)
        mapper.SetLabelModeToLabelFieldData()
        mapper.SetFieldDataName('labels')
        mapper.GetLabelTextProperty().SetColor(*self.options.text_color)
        mapper.GetLabelTextProperty().SetFontSize(14)

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        self.renderer.AddActor(actor)

    def show(self):
        self.window.Render()
        self.interactor.Initialize()
        self.interactor.Start()
        return self

    def render(self):
        self.window.Render()
        return self

    def save_screenshot(self, path, *, scale=1):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        self.window.SetOffScreenRendering(1)
        self.window.Render()

        capture = vtk.vtkWindowToImageFilter()
        capture.SetInput(self.window)
        capture.SetScale(int(scale))
        capture.SetInputBufferTypeToRGB()
        capture.ReadFrontBufferOff()
        capture.Update()

        writer = vtk.vtkPNGWriter()
        writer.SetFileName(str(path))
        writer.SetInputConnection(capture.GetOutputPort())
        writer.Write()
        return path

    def close(self):
        self.window.Finalize()
        self.interactor.TerminateApp()


def view_mesh(mesh, *, options=None):
    return VTKMeshViewer(mesh, options=options).show()
