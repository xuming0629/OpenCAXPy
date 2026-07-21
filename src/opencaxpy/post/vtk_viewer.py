from .vtk_converter import VtkConverter
class VtkViewer:
    @staticmethod
    def show(mesh, *, scalars=None, show_edges=True, show_node_ids=False, show_cell_ids=False):
        try: import pyvista as pv
        except ImportError as exc: raise ImportError('Run: pip install pyvista') from exc
        grid=VtkConverter.to_pyvista(mesh); plotter=pv.Plotter(); plotter.add_mesh(grid,scalars=scalars,show_edges=show_edges)
        if show_node_ids: plotter.add_point_labels(grid.points,[str(i) for i in range(mesh.num_nodes)])
        if show_cell_ids: plotter.add_point_labels(grid.cell_centers().points,[str(i) for i in range(mesh.num_cells)])
        plotter.show(); return plotter
