import xml.etree.ElementTree as ET
import numpy as np
from opencaxpy import VtkConverter, rectangle_triangle
def test_vtk_arrays_and_export(tmp_path):
    mesh=rectangle_triangle(0,1,0,1,1,1); mesh.point_data['u']=np.arange(mesh.num_nodes,dtype=float)
    a=VtkConverter.arrays(mesh); assert a['points'].shape==(mesh.num_nodes,3); assert a['cell_types'].tolist()==[5,5]
    out=mesh.write_vtu(tmp_path/'triangle.vtu'); assert out.exists(); piece=ET.parse(out).getroot().find('./UnstructuredGrid/Piece'); assert piece.attrib['NumberOfCells']==str(mesh.num_cells)
