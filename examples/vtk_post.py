import numpy as np
import opencaxpy as ocx
mesh=ocx.box_tetra(0,1,0,1,0,1,2,2,2)
p=mesh.backend.to_numpy(mesh.points)
mesh.point_data['temperature']=mesh.backend.asarray(p[:,0]+p[:,1]+p[:,2],device=mesh.device)
print(mesh.write_vtu('outputs/tetra_temperature.vtu'))
# mesh.show(scalars='temperature', show_edges=True)
