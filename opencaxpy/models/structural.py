import numpy as np


class StructuralModel:
    def __init__(self, points, dofs_per_node):
        self.points = np.asarray(points, float)
        self.dofs_per_node = int(dofs_per_node)
        self.elements = []
        self.loads = {}
        self.constraints = {}

    @property
    def ndof(self):
        return len(self.points) * self.dofs_per_node

    def add_element(self, e):
        if e.dofs_per_node != self.dofs_per_node:
            raise ValueError("uniform nodal DOF count required in v1.1 high-level structural model")
        self.elements.append(e)

    def add_load(self, dof, value):
        self.loads[dof] = self.loads.get(dof, 0.0) + float(value)

    def constrain(self, dof, value=0.0):
        self.constraints[int(dof)] = float(value)

    def load_vector(self):
        f = np.zeros(self.ndof)
        for i, v in self.loads.items():
            f[i] += v
        return f
