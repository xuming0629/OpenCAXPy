from __future__ import annotations

from pathlib import Path

import numpy as np
import vtk

from vtkmodules.util.numpy_support import numpy_to_vtk

from .options import VTKMeshViewerOptions
from .vtk_adapter import (
    make_point_cloud,
    make_polydata_from_entities,
    to_vtk_unstructured_grid,
)


class VTKMeshViewer:
    """VTK-native mesh viewer for OpenCAXPy.

    The mesh kernel has no dependency on VTK.
    Only this visualization package performs the conversion to
    vtkUnstructuredGrid / vtkPolyData.
    """

    def __init__(self, mesh, options=None):
        self.mesh = mesh
        self.options = options or VTKMeshViewerOptions()

        # ---------------------------------------------------------
        # VTK core objects
        # ---------------------------------------------------------
        self.renderer = vtk.vtkRenderer()

        self.window = vtk.vtkRenderWindow()
        self.window.SetWindowName(self.options.title)
        self.window.SetSize(*self.options.window_size)
        self.window.AddRenderer(self.renderer)

        self.interactor = vtk.vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.window)

        style = vtk.vtkInteractorStyleTrackballCamera()
        self.interactor.SetInteractorStyle(style)

        # ---------------------------------------------------------
        # Persistent visualization objects
        # ---------------------------------------------------------
        self.grid = None

        self.surface_mapper = None
        self.surface_actor = None

        self.edge_mapper = None
        self.edge_actor = None

        self.node_mapper = None
        self.node_actor = None

        self.scalar_bar = None

        self._orientation_widget = None

        self._build_scene()

    # =============================================================
    # Scene
    # =============================================================

    def _build_scene(self):
        o = self.options

        self.renderer.SetBackground(*o.background)

        # IMPORTANT:
        # 保存 grid，后续 scalar / vector field 都需要使用
        self.grid = to_vtk_unstructured_grid(self.mesh)

        # ---------------------------------------------------------
        # Surface / Cell
        # ---------------------------------------------------------
        if o.show_surface:

            if o.show_boundary_only and self.mesh.topological_dimension == 3:
                mapper = vtk.vtkPolyDataMapper()

                poly = make_polydata_from_entities(
                    self.mesh,
                    "face",
                    self.mesh.boundary_face_index(),
                )

                mapper.SetInputData(poly)

            else:
                mapper = vtk.vtkDataSetMapper()
                mapper.SetInputData(self.grid)

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)

            actor.GetProperty().SetColor(*o.surface_color)

            actor.GetProperty().SetOpacity(o.surface_opacity)

            self.renderer.AddActor(actor)

            self.surface_mapper = mapper
            self.surface_actor = actor

        # ---------------------------------------------------------
        # Edges
        # ---------------------------------------------------------
        if o.show_edges:

            edge_ids = None

            if o.show_boundary_only:
                edge_ids = self.mesh.boundary_edge_index()

            edge_poly = make_polydata_from_entities(
                self.mesh,
                "edge",
                edge_ids,
            )

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(edge_poly)

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)

            actor.GetProperty().SetColor(*o.edge_color)

            actor.GetProperty().SetLineWidth(o.line_width)

            self.renderer.AddActor(actor)

            self.edge_mapper = mapper
            self.edge_actor = actor

        # ---------------------------------------------------------
        # Nodes
        # ---------------------------------------------------------
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

            self.node_mapper = mapper
            self.node_actor = actor

        # ---------------------------------------------------------
        # Labels
        # ---------------------------------------------------------
        if o.show_node_ids:

            self._add_labels(
                self.mesh.points,
                [f"N{i}" for i in range(self.mesh.number_of_nodes())],
            )

        if o.show_edge_ids:

            centers = self.mesh.entity_barycenter("edge")

            self._add_labels(
                centers,
                [f"E{i}" for i in range(self.mesh.number_of_edges())],
            )

        if o.show_face_ids and self.mesh.topological_dimension == 3:

            centers = self.mesh.entity_barycenter("face")

            self._add_labels(
                centers,
                [f"F{i}" for i in range(self.mesh.number_of_faces())],
            )

        if o.show_cell_ids:

            centers = self.mesh.entity_barycenter("cell")

            self._add_labels(
                centers,
                [f"C{i}" for i in range(self.mesh.number_of_cells())],
            )

        # ---------------------------------------------------------
        # Axes
        # ---------------------------------------------------------
        axes = vtk.vtkAxesActor()

        widget = vtk.vtkOrientationMarkerWidget()
        widget.SetOrientationMarker(axes)
        widget.SetInteractor(self.interactor)
        widget.SetViewport(
            0.0,
            0.0,
            0.18,
            0.18,
        )

        widget.SetEnabled(1)
        widget.InteractiveOff()

        self._orientation_widget = widget

        self.renderer.ResetCamera()

    # =============================================================
    # Scalar field
    # =============================================================

    def add_point_scalar(
        self,
        name: str,
        values,
        *,
        show_scalar_bar: bool = True,
    ):
        """Add nodal scalar field to the mesh.

        Parameters
        ----------
        name:
            Scalar field name.

        values:
            Scalar values defined on mesh nodes.

        show_scalar_bar:
            Whether to display scalar bar.
        """

        values = np.asarray(
            values,
            dtype=np.float64,
        ).reshape(-1)

        num_points = self.grid.GetNumberOfPoints()

        if values.size != num_points:
            raise ValueError(
                f"Point scalar '{name}' has "
                f"{values.size} values, "
                f"but mesh has {num_points} nodes."
            )

        vtk_array = numpy_to_vtk(
            values,
            deep=True,
            array_type=vtk.VTK_DOUBLE,
        )

        vtk_array.SetName(name)

        point_data = self.grid.GetPointData()

        if point_data.HasArray(name):
            point_data.RemoveArray(name)

        point_data.AddArray(vtk_array)
        point_data.SetActiveScalars(name)

        self.grid.Modified()

        # ---------------------------------------------------------
        # Surface coloring
        # ---------------------------------------------------------
        if self.surface_mapper is not None:

            self.surface_mapper.SetScalarVisibility(True)

            self.surface_mapper.SetScalarModeToUsePointData()

            self.surface_mapper.SelectColorArray(name)

            vmin = float(np.min(values))
            vmax = float(np.max(values))

            if np.isclose(vmin, vmax):
                vmax = vmin + 1.0e-12

            self.surface_mapper.SetScalarRange(
                vmin,
                vmax,
            )

            # 使用 VTK 默认 lookup table
            lookup_table = vtk.vtkLookupTable()
            lookup_table.SetNumberOfTableValues(256)
            lookup_table.SetRange(vmin, vmax)
            lookup_table.Build()

            self.surface_mapper.SetLookupTable(lookup_table)

        if show_scalar_bar:
            self._add_scalar_bar(name)

        self.render()

        return self

    def add_cell_scalar(
        self,
        name: str,
        values,
        *,
        show_scalar_bar: bool = True,
    ):
        """Add cell scalar field."""

        values = np.asarray(
            values,
            dtype=np.float64,
        ).reshape(-1)

        num_cells = self.grid.GetNumberOfCells()

        if values.size != num_cells:
            raise ValueError(
                f"Cell scalar '{name}' has "
                f"{values.size} values, "
                f"but mesh has {num_cells} cells."
            )

        vtk_array = numpy_to_vtk(
            values,
            deep=True,
            array_type=vtk.VTK_DOUBLE,
        )

        vtk_array.SetName(name)

        cell_data = self.grid.GetCellData()

        if cell_data.HasArray(name):
            cell_data.RemoveArray(name)

        cell_data.AddArray(vtk_array)
        cell_data.SetActiveScalars(name)

        self.grid.Modified()

        if self.surface_mapper is not None:

            self.surface_mapper.SetScalarVisibility(True)

            self.surface_mapper.SetScalarModeToUseCellData()

            self.surface_mapper.SelectColorArray(name)

            vmin = float(np.min(values))
            vmax = float(np.max(values))

            if np.isclose(vmin, vmax):
                vmax = vmin + 1.0e-12

            self.surface_mapper.SetScalarRange(
                vmin,
                vmax,
            )

            lookup_table = vtk.vtkLookupTable()
            lookup_table.SetNumberOfTableValues(256)
            lookup_table.SetRange(vmin, vmax)
            lookup_table.Build()

            self.surface_mapper.SetLookupTable(lookup_table)

        if show_scalar_bar:
            self._add_scalar_bar(name)

        self.render()

        return self

    # =============================================================
    # Scalar bar
    # =============================================================

    def _add_scalar_bar(self, name: str):

        if self.surface_mapper is None:
            return

        if self.scalar_bar is not None:
            self.renderer.RemoveActor2D(self.scalar_bar)

        scalar_bar = vtk.vtkScalarBarActor()

        scalar_bar.SetLookupTable(self.surface_mapper.GetLookupTable())

        scalar_bar.SetTitle(name)

        scalar_bar.SetNumberOfLabels(5)

        scalar_bar.SetWidth(0.10)
        scalar_bar.SetHeight(0.55)

        scalar_bar.SetPosition(
            0.87,
            0.20,
        )

        scalar_bar.GetTitleTextProperty().SetColor(*self.options.text_color)

        scalar_bar.GetLabelTextProperty().SetColor(*self.options.text_color)

        self.renderer.AddActor2D(scalar_bar)

        self.scalar_bar = scalar_bar

    # =============================================================
    # Labels
    # =============================================================

    def _add_labels(
        self,
        points,
        labels,
    ):

        points = np.asarray(
            points,
            dtype=float,
        )

        if points.shape[1] == 1:

            points = np.column_stack(
                [
                    points[:, 0],
                    np.zeros((len(points), 2)),
                ]
            )

        elif points.shape[1] == 2:

            points = np.column_stack(
                [
                    points,
                    np.zeros(len(points)),
                ]
            )

        vtk_points = vtk.vtkPoints()

        for p in points:

            vtk_points.InsertNextPoint(
                float(p[0]),
                float(p[1]),
                float(p[2]),
            )

        poly = vtk.vtkPolyData()
        poly.SetPoints(vtk_points)

        label_array = vtk.vtkStringArray()
        label_array.SetName("labels")

        for label in labels:
            label_array.InsertNextValue(str(label))

        poly.GetPointData().AddArray(label_array)

        mapper = vtk.vtkLabeledDataMapper()
        mapper.SetInputData(poly)

        mapper.SetLabelModeToLabelFieldData()

        mapper.SetFieldDataName("labels")

        mapper.GetLabelTextProperty().SetColor(*self.options.text_color)

        mapper.GetLabelTextProperty().SetFontSize(14)

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)

        self.renderer.AddActor(actor)

    # =============================================================
    # Render
    # =============================================================

    def show(self):

        self.window.Render()

        self.interactor.Initialize()

        self.interactor.Start()

        return self

    def render(self):

        self.window.Render()

        return self

    # =============================================================
    # Screenshot
    # =============================================================

    def save_screenshot(
        self,
        path,
        *,
        scale=1,
    ):

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

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

    # =============================================================
    # Close
    # =============================================================

    def close(self):

        self.window.Finalize()

        self.interactor.TerminateApp()


def view_mesh(
    mesh,
    *,
    options=None,
):
    return VTKMeshViewer(
        mesh,
        options=options,
    ).show()
