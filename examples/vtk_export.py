from opencaxpy import MeshFactory, refine

mesh = MeshFactory.tetra_box(nx=1, ny=1, nz=1)
mesh = refine(mesh, method="uniform").mesh
mesh.viewer().write_vtu("refined_tetra.vtu")
