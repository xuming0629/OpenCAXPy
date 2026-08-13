from __future__ import annotations
from pathlib import Path
import math
import matplotlib.pyplot as plt
import vtk
from .options import FigureOptions
from .backend.vtk_renderer import VTKRenderContext, capture_renderer


class Figure:
    """Compose MeshPlot, SolutionPlot and ConvergencePlot in one layout."""
    def __init__(self, *, layout=None, options=None, title=None):
        self.layout=layout
        self.options=options or FigureOptions()
        if title is not None: self.options.title=title
        self.plots=[]

    def add(self, plot, *, row=None, col=None):
        self.plots.append((plot,row,col)); return self

    def _shape(self):
        if self.layout is not None: return tuple(self.layout)
        n=max(1,len(self.plots)); cols=min(3,n); rows=math.ceil(n/cols); return rows,cols

    def show(self, *, save_path=None, interactive=True):
        kinds={p.backend for p,_,_ in self.plots}
        if kinds == {"vtk"} and interactive and save_path is None:
            return self._show_vtk()
        return self._show_composite(save_path=save_path, show=interactive)

    def save(self,path):
        return self._show_composite(save_path=path,show=False)

    def _show_vtk(self):
        rows,cols=self._shape(); win=vtk.vtkRenderWindow(); win.SetSize(*self.options.window_size); win.SetWindowName(self.options.title or "OpenCAXPy Visualization")
        inter=vtk.vtkRenderWindowInteractor(); inter.SetRenderWindow(win); inter.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        for idx,(plot,row,col) in enumerate(self.plots):
            r=idx//cols if row is None else row; c=idx%cols if col is None else col
            ren=vtk.vtkRenderer(); ren.SetViewport(c/cols,1-(r+1)/rows,(c+1)/cols,1-r/rows); win.AddRenderer(ren); plot.render(VTKRenderContext(ren,inter))
        win.Render(); inter.Initialize(); inter.Start(); return self

    def _show_composite(self, *, save_path=None, show=True):
        rows,cols=self._shape(); fig,axes=plt.subplots(rows,cols,figsize=self.options.figsize,squeeze=False)
        if self.options.title: fig.suptitle(self.options.title)
        for idx,(plot,row,col) in enumerate(self.plots):
            r=idx//cols if row is None else row; c=idx%cols if col is None else col; ax=axes[r][c]
            if plot.backend=="matplotlib":
                C=type("MatplotlibContext",(),{"ax":ax})(); plot.render(C)
            elif plot.backend=="vtk":
                ax.imshow(capture_renderer(plot)); ax.set_axis_off();
                if plot.title: ax.set_title(plot.title)
            else: raise ValueError(f"Unsupported backend {plot.backend}")
        for idx in range(len(self.plots),rows*cols): axes[idx//cols][idx%cols].set_visible(False)
        fig.tight_layout()
        if save_path is not None:
            p=Path(save_path); p.parent.mkdir(parents=True,exist_ok=True); fig.savefig(p,dpi=self.options.dpi,bbox_inches="tight")
        if show: plt.show()
        return fig,axes
