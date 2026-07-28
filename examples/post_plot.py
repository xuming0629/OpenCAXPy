import numpy as np
from opencaxpy import TriangleMesh

mesh = TriangleMesh(
    [[0,0], [1,0], [0,1], [1,1]],
    [[0,1,2], [1,3,2]],
)

mesh.cell_data["quality"] = np.array([0.8, 1.0])

mesh.plot(
    show_nodes=True,
    show_boundary=True,
    show_node_ids=True,
    show_cell_ids=True,
    scalar_name="quality",
    scalar_location="cell",
    title="OpenCAXPy Triangle Mesh",
)
