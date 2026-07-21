import numpy as np
from .vtk_types import VTK_CELL_TYPES
class VtkConverter:
    @staticmethod
    def arrays(mesh):
        points=mesh.backend.to_numpy(mesh.points).astype(np.float64,copy=False)
        cells=mesh.backend.to_numpy(mesh.cells).astype(np.int64,copy=False)
        if points.shape[1]==2: points=np.column_stack((points,np.zeros(points.shape[0])))
        if points.shape[1]!=3: raise ValueError('VTK conversion requires 2D or 3D points')
        return {'points':points,'cells':cells,'connectivity':cells.reshape(-1),'offsets':np.arange(1,mesh.num_cells+1,dtype=np.int64)*cells.shape[1],'cell_types':np.full(mesh.num_cells,VTK_CELL_TYPES[mesh.cell_type],dtype=np.uint8)}
    @staticmethod
    def to_pyvista(mesh):
        try: import pyvista as pv
        except ImportError as exc: raise ImportError('Run: pip install pyvista') from exc
        a=VtkConverter.arrays(mesh); legacy=np.column_stack((np.full(mesh.num_cells,a['cells'].shape[1],dtype=np.int64),a['cells'])).reshape(-1)
        grid=pv.UnstructuredGrid(legacy,a['cell_types'],a['points'])
        for n,v in mesh.point_data.items(): grid.point_data[n]=mesh.backend.to_numpy(v)
        for n,v in mesh.cell_data.items(): grid.cell_data[n]=mesh.backend.to_numpy(v)
        return grid
