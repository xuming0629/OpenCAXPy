import numpy as np
class SourceIntegrator:
    def __init__(self, source=0.0): self.source=source
    def cell_vector(self, mesh, ci):
        coords=mesh.cell_coordinates(ci)
        xbar=coords.mean(axis=0)
        f=self.source(xbar) if callable(self.source) else self.source
        m=mesh.entity_measure()[ci]
        return np.full(len(mesh.cells[ci]), float(f)*m/len(mesh.cells[ci]))
