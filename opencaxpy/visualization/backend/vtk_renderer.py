from __future__ import annotations
import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk, vtk_to_numpy
from ..vtk_adapter import to_vtk_unstructured_grid, points_3d


class VTKRenderContext:
    def __init__(self, renderer, interactor=None):
        self.renderer=renderer; self.interactor=interactor
        self.scalar_bars=[]; self.orientation_widgets=[]

    def render_mesh(self, plot):
        o=plot.style; t=o.theme
        self.renderer.SetBackground(*t.background)
        grid=to_vtk_unstructured_grid(plot.mesh)
        mapper=vtk.vtkDataSetMapper(); mapper.SetInputData(grid); mapper.ScalarVisibilityOff()
        actor=vtk.vtkActor(); actor.SetMapper(mapper)
        actor.GetProperty().SetColor(*t.surface_color); actor.GetProperty().SetOpacity(o.surface_opacity)
        if o.show_surface:
            actor.GetProperty().SetRepresentationToSurface()
        else:
            actor.GetProperty().SetRepresentationToWireframe()
        if o.show_edges:
            actor.GetProperty().EdgeVisibilityOn(); actor.GetProperty().SetEdgeColor(*t.edge_color); actor.GetProperty().SetLineWidth(o.line_width)
        self.renderer.AddActor(actor)
        if o.show_nodes:
            self._add_nodes(plot.mesh.points,o)
        self._labels(plot.mesh,o)
        self._title(plot.title)
        self.renderer.ResetCamera()
        return actor

    def render_solution(self, plot):
        ms=plot.mesh_style; t=ms.theme
        self.renderer.SetBackground(*t.background)
        grid=to_vtk_unstructured_grid(plot.mesh)
        f=plot.solution[plot.field]
        values=f.component(plot.component)
        arr=np.asarray(values,float)
        if arr.ndim != 1:
            if f.kind == "vector": arr=np.linalg.norm(arr,axis=1)
            else: raise ValueError("Select a scalar component for tensor/vector fields")
        target=grid.GetPointData() if f.location=="point" else grid.GetCellData()
        va=numpy_to_vtk(np.ascontiguousarray(arr),deep=True,array_type=vtk.VTK_DOUBLE)
        display_name=f.name if plot.component is None else f"{f.name}.{plot.component}"
        va.SetName(display_name); target.AddArray(va); target.SetActiveScalars(display_name)
        display_grid=grid
        if plot.deformation is not None:
            df=plot.solution[plot.deformation]
            dv=np.asarray(df.values,float)
            if dv.ndim==1: dv=dv.reshape(grid.GetNumberOfPoints(),-1)
            dv=points_3d(dv)
            da=numpy_to_vtk(np.ascontiguousarray(dv),deep=True,array_type=vtk.VTK_DOUBLE); da.SetName("__deformation__")
            grid.GetPointData().AddArray(da); grid.GetPointData().SetActiveVectors("__deformation__")
            scale=self._deformation_scale(grid,dv,plot.scale)
            warp=vtk.vtkWarpVector(); warp.SetInputData(grid); warp.SetInputArrayToProcess(0,0,0,vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS,"__deformation__"); warp.SetScaleFactor(scale); warp.Update()
            display_grid=warp.GetOutput()
            if plot.deformation_style.show_undeformed: self._undeformed(grid,plot)
        mapper=vtk.vtkDataSetMapper(); mapper.SetInputData(display_grid)
        if f.location=="point": mapper.SetScalarModeToUsePointData()
        else: mapper.SetScalarModeToUseCellData()
        mapper.SelectColorArray(display_name); mapper.ScalarVisibilityOn()
        lo,hi=float(np.min(arr)),float(np.max(arr))
        if plot.field_style.scalar_range is not None: lo,hi=plot.field_style.scalar_range
        if np.isclose(lo,hi): hi=lo+1e-12
        lut=vtk.vtkLookupTable(); lut.SetNumberOfTableValues(256); lut.SetRange(lo,hi); lut.Build()
        mapper.SetLookupTable(lut); mapper.SetScalarRange(lo,hi)
        actor=vtk.vtkActor(); actor.SetMapper(mapper); actor.GetProperty().SetOpacity(ms.surface_opacity)
        if ms.show_edges:
            actor.GetProperty().EdgeVisibilityOn(); actor.GetProperty().SetEdgeColor(*t.edge_color); actor.GetProperty().SetLineWidth(ms.line_width)
        self.renderer.AddActor(actor)
        if ms.show_nodes: self._add_nodes(points_3d(plot.mesh.points),ms)
        if plot.field_style.show_scalar_bar: self._scalar_bar(display_name,lut,plot.field_style.scalar_bar_labels,t.text_color)
        self._title(plot.title or display_name); self.renderer.ResetCamera()
        return actor

    def _deformation_scale(self,grid,dv,scale):
        if scale != "auto": return float(scale)
        pts=vtk_to_numpy(grid.GetPoints().GetData()); diag=np.linalg.norm(pts.max(0)-pts.min(0)); umax=np.linalg.norm(dv,axis=1).max()
        return 1.0 if umax<=1e-15 else 0.08*diag/umax

    def _undeformed(self,grid,plot):
        m=vtk.vtkDataSetMapper(); m.SetInputData(grid); m.ScalarVisibilityOff()
        a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetRepresentationToWireframe(); a.GetProperty().SetColor(*plot.mesh_style.theme.undeformed_color); a.GetProperty().SetOpacity(plot.deformation_style.undeformed_opacity); a.GetProperty().SetLineWidth(plot.deformation_style.undeformed_line_width); self.renderer.AddActor(a)

    def _add_nodes(self,points,o):
        pts=vtk.vtkPoints(); pts.SetData(numpy_to_vtk(points_3d(points),deep=True))
        poly=vtk.vtkPolyData(); poly.SetPoints(pts); glyph=vtk.vtkVertexGlyphFilter(); glyph.SetInputData(poly); glyph.Update()
        m=vtk.vtkPolyDataMapper(); m.SetInputConnection(glyph.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*o.theme.node_color); a.GetProperty().SetPointSize(o.point_size); self.renderer.AddActor(a)

    def _labels(self,mesh,o):
        if o.show_node_ids: self._add_label_points(mesh.points,[f"N{i}" for i in range(len(mesh.points))],o.theme.text_color)
        for flag,etype,prefix in [(o.show_edge_ids,"edge","E"),(o.show_face_ids,"face","F"),(o.show_cell_ids,"cell","C")]:
            if flag and hasattr(mesh,"entity_barycenter"):
                try: p=mesh.entity_barycenter(etype)
                except Exception: continue
                self._add_label_points(p,[f"{prefix}{i}" for i in range(len(p))],o.theme.text_color)

    def _add_label_points(self,p,labels,color):
        p=points_3d(p); pts=vtk.vtkPoints(); [pts.InsertNextPoint(*map(float,x)) for x in p]
        poly=vtk.vtkPolyData(); poly.SetPoints(pts); sa=vtk.vtkStringArray(); sa.SetName("labels"); [sa.InsertNextValue(str(x)) for x in labels]; poly.GetPointData().AddArray(sa)
        m=vtk.vtkLabeledDataMapper(); m.SetInputData(poly); m.SetLabelModeToLabelFieldData(); m.SetFieldDataName("labels"); m.GetLabelTextProperty().SetColor(*color); m.GetLabelTextProperty().SetFontSize(14)
        a=vtk.vtkActor2D(); a.SetMapper(m); self.renderer.AddActor(a)

    def _scalar_bar(self,title,lut,nlabels,color):
        b=vtk.vtkScalarBarActor(); b.SetLookupTable(lut); b.SetTitle(title); b.SetNumberOfLabels(nlabels); b.SetWidth(.10); b.SetHeight(.55); b.SetPosition(.87,.20); b.GetTitleTextProperty().SetColor(*color); b.GetLabelTextProperty().SetColor(*color); self.renderer.AddActor2D(b); self.scalar_bars.append(b)

    def _title(self,title):
        if not title: return
        a=vtk.vtkTextActor(); a.SetInput(str(title)); a.GetTextProperty().SetFontSize(18); a.GetTextProperty().SetColor(.15,.15,.15); a.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport(); a.SetPosition(.03,.94); self.renderer.AddActor2D(a)


def capture_renderer(plot, width=700, height=520):
    win=vtk.vtkRenderWindow(); win.SetOffScreenRendering(1); win.SetSize(width,height)
    ren=vtk.vtkRenderer(); win.AddRenderer(ren); ctx=VTKRenderContext(ren); plot.render(ctx); win.Render()
    f=vtk.vtkWindowToImageFilter(); f.SetInput(win); f.SetInputBufferTypeToRGB(); f.ReadFrontBufferOff(); f.Update()
    im=f.GetOutput(); w,h,_=im.GetDimensions(); arr=vtk_to_numpy(im.GetPointData().GetScalars()).reshape(h,w,3); arr=np.flipud(arr.copy()); win.Finalize(); return arr
