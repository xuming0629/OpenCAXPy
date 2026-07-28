from __future__ import annotations

from pathlib import Path

from .options import ViewerOptions


class Viewer:
    def __init__(
        self,
        mesh,
        options: ViewerOptions | None = None,
        **kwargs,
    ) -> None:
        self.mesh = mesh
        self.options = options or ViewerOptions(**kwargs)

    @staticmethod
    def _vtk():
        try:
            import vtk
        except ImportError as exc:
            raise ImportError(
                "VTK support requires `pip install opencaxpy[vtk]`"
            ) from exc
        return vtk

    def _create_id_filter(self):
        """Create a VTK point/cell ID generator across VTK versions.

        VTK 9.4+ uses vtkGenerateIds, while older VTK releases use
        vtkIdFilter.
        """
        vtk = self._vtk()

        if hasattr(vtk, "vtkGenerateIds"):
            return vtk.vtkGenerateIds()

        if hasattr(vtk, "vtkIdFilter"):
            return vtk.vtkIdFilter()

        raise RuntimeError(
            "Current VTK installation provides neither "
            "vtkGenerateIds nor vtkIdFilter"
        )

    @staticmethod
    def _enable_field_data(ids) -> None:
        """Request generated IDs as named field-data arrays when supported."""
        if hasattr(ids, "FieldDataOn"):
            ids.FieldDataOn()

    def build_grid(self):
        vtk = self._vtk()
        points_np = self.mesh.backend.to_numpy(self.mesh.points)
        cells_np = self.mesh.backend.to_numpy(self.mesh.cells)

        vtk_points = vtk.vtkPoints()
        for point in points_np:
            xyz = list(map(float, point)) + [0.0, 0.0, 0.0]
            vtk_points.InsertNextPoint(xyz[0], xyz[1], xyz[2])

        grid = vtk.vtkUnstructuredGrid()
        grid.SetPoints(vtk_points)

        vtk_types = {
            "triangle3": vtk.VTK_TRIANGLE,
            "triangle6": vtk.VTK_QUADRATIC_TRIANGLE,
            "quad4": vtk.VTK_QUAD,
            "quad8": vtk.VTK_QUADRATIC_QUAD,
            "quad9": vtk.VTK_BIQUADRATIC_QUAD,
            "tetra4": vtk.VTK_TETRA,
            "hexa8": vtk.VTK_HEXAHEDRON,
        }
        vtk_type = vtk_types.get(self.mesh.cell_type.name)
        if vtk_type is None:
            raise NotImplementedError(
                f"VTK conversion is not implemented for "
                f"{self.mesh.cell_type.name}"
            )

        for cell in cells_np:
            ids = vtk.vtkIdList()
            for node_id in cell:
                ids.InsertNextId(int(node_id))
            grid.InsertNextCell(vtk_type, ids)

        self._attach_all_data(grid)
        return grid

    def _attach_all_data(self, grid):
        import numpy as np
        from vtk.util.numpy_support import numpy_to_vtk

        for name, values in self.mesh.point_data.items():
            arr = np.asarray(self.mesh.backend.to_numpy(values))
            vtk_arr = numpy_to_vtk(arr, deep=True)
            vtk_arr.SetName(name)
            grid.GetPointData().AddArray(vtk_arr)

        for name, values in self.mesh.cell_data.items():
            arr = np.asarray(self.mesh.backend.to_numpy(values))
            vtk_arr = numpy_to_vtk(arr, deep=True)
            vtk_arr.SetName(name)
            grid.GetCellData().AddArray(vtk_arr)

        if self.options.scalar_name:
            if self.options.scalar_location == "point":
                grid.GetPointData().SetActiveScalars(
                    self.options.scalar_name
                )
            else:
                grid.GetCellData().SetActiveScalars(
                    self.options.scalar_name
                )

    def _add_node_actor(self, renderer, grid):
        if not self.options.show_nodes:
            return

        vtk = self._vtk()
        glyph = vtk.vtkVertexGlyphFilter()
        glyph.SetInputData(grid)
        glyph.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(glyph.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetPointSize(self.options.node_size)
        actor.GetProperty().SetColor(*self.options.node_color)
        renderer.AddActor(actor)

    def _add_boundary_actor(self, renderer, grid):
        if not self.options.show_boundary:
            return

        vtk = self._vtk()
        geometry = vtk.vtkGeometryFilter()
        geometry.SetInputData(grid)
        geometry.Update()

        feature = vtk.vtkFeatureEdges()
        feature.SetInputConnection(geometry.GetOutputPort())
        feature.BoundaryEdgesOn()
        feature.FeatureEdgesOff()
        feature.NonManifoldEdgesOn()
        feature.ManifoldEdgesOff()
        feature.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(feature.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(*self.options.boundary_color)
        actor.GetProperty().SetLineWidth(self.options.boundary_width)
        renderer.AddActor(actor)

    def _label_text_property(self, mapper, color, font_size):
        prop = mapper.GetLabelTextProperty()
        prop.SetColor(*color)
        prop.SetFontSize(int(font_size))
        prop.SetBold(True)
        prop.SetShadow(False)

    def _add_node_labels(self, renderer, grid):
        if not self.options.show_node_ids:
            return

        vtk = self._vtk()
        ids = self._create_id_filter()
        ids.SetInputData(grid)
        ids.PointIdsOn()
        ids.CellIdsOff()
        self._enable_field_data(ids)
        ids.SetPointIdsArrayName("NodeIds")
        ids.Update()

        glyph = vtk.vtkVertexGlyphFilter()
        glyph.SetInputConnection(ids.GetOutputPort())
        glyph.Update()

        mapper = vtk.vtkLabeledDataMapper()
        mapper.SetInputConnection(glyph.GetOutputPort())
        mapper.SetLabelModeToLabelFieldData()
        mapper.SetFieldDataName("NodeIds")
        self._label_text_property(
            mapper,
            self.options.node_label_color,
            self.options.node_label_font_size,
        )

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        renderer.AddActor2D(actor)

    def _add_cell_labels(self, renderer, grid):
        if not self.options.show_cell_ids:
            return

        vtk = self._vtk()
        ids = self._create_id_filter()
        ids.SetInputData(grid)
        ids.PointIdsOff()
        ids.CellIdsOn()
        self._enable_field_data(ids)
        ids.SetCellIdsArrayName("CellIds")
        ids.Update()

        centers = vtk.vtkCellCenters()
        centers.SetInputConnection(ids.GetOutputPort())
        centers.Update()

        mapper = vtk.vtkLabeledDataMapper()
        mapper.SetInputConnection(centers.GetOutputPort())
        mapper.SetLabelModeToLabelFieldData()
        mapper.SetFieldDataName("CellIds")
        self._label_text_property(
            mapper,
            self.options.cell_label_color,
            self.options.cell_label_font_size,
        )

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        renderer.AddActor2D(actor)

    def _add_edge_labels(self, renderer, grid):
        if not self.options.show_edge_ids:
            return

        vtk = self._vtk()

        extract = vtk.vtkExtractEdges()
        extract.SetInputData(grid)
        extract.Update()

        edges = extract.GetOutput()

        ids = vtk.vtkIntArray()
        ids.SetName("EdgeIds")
        ids.SetNumberOfComponents(1)
        ids.SetNumberOfTuples(edges.GetNumberOfCells())
        for edge_id in range(edges.GetNumberOfCells()):
            ids.SetValue(edge_id, edge_id)
        edges.GetCellData().AddArray(ids)

        centers = vtk.vtkCellCenters()
        centers.SetInputData(edges)
        centers.Update()

        mapper = vtk.vtkLabeledDataMapper()
        mapper.SetInputConnection(centers.GetOutputPort())
        mapper.SetLabelModeToLabelFieldData()
        mapper.SetFieldDataName("EdgeIds")
        self._label_text_property(
            mapper,
            self.options.edge_label_color,
            self.options.edge_label_font_size,
        )

        actor = vtk.vtkActor2D()
        actor.SetMapper(mapper)
        renderer.AddActor2D(actor)

    def _scene(self):
        vtk = self._vtk()
        grid = self.build_grid()

        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(grid)
        mapper.SetScalarVisibility(bool(self.options.scalar_name))

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(*self.options.surface_color)
        actor.GetProperty().SetEdgeColor(*self.options.edge_color)
        actor.GetProperty().SetLineWidth(self.options.edge_width)

        if self.options.show_edges:
            actor.GetProperty().EdgeVisibilityOn()
        else:
            actor.GetProperty().EdgeVisibilityOff()

        renderer = vtk.vtkRenderer()
        renderer.AddActor(actor)
        renderer.SetBackground(*self.options.background_color)

        self._add_node_actor(renderer, grid)
        self._add_boundary_actor(renderer, grid)
        self._add_node_labels(renderer, grid)
        self._add_edge_labels(renderer, grid)
        self._add_cell_labels(renderer, grid)

        if self.options.scalar_name and self.options.show_scalar_bar:
            scalar_bar = vtk.vtkScalarBarActor()
            scalar_bar.SetLookupTable(mapper.GetLookupTable())
            scalar_bar.SetTitle(self.options.scalar_name)
            renderer.AddActor2D(scalar_bar)

        window = vtk.vtkRenderWindow()
        window.SetWindowName(self.options.title)
        window.SetSize(*self.options.window_size)
        window.AddRenderer(renderer)
        renderer.ResetCamera()

        return grid, renderer, window

    def show(self) -> None:
        vtk = self._vtk()
        _, _, window = self._scene()

        interactor = vtk.vtkRenderWindowInteractor()
        interactor.SetRenderWindow(window)

        window.Render()
        interactor.Initialize()
        interactor.Start()

    def screenshot(
        self,
        filename,
        *,
        magnification: int = 1,
    ) -> Path:
        vtk = self._vtk()
        _, _, window = self._scene()

        window.SetOffScreenRendering(1)
        window.Render()

        capture = vtk.vtkWindowToImageFilter()
        capture.SetInput(window)
        capture.SetScale(int(magnification))
        capture.Update()

        writer = vtk.vtkPNGWriter()
        writer.SetFileName(str(filename))
        writer.SetInputConnection(capture.GetOutputPort())
        writer.Write()

        return Path(filename)

    def write_vtu(self, filename) -> Path:
        vtk = self._vtk()
        grid = self.build_grid()

        writer = vtk.vtkXMLUnstructuredGridWriter()
        writer.SetFileName(str(filename))
        writer.SetInputData(grid)

        if writer.Write() != 1:
            raise OSError(f"failed to write {filename}")

        return Path(filename)
