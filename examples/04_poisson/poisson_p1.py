# import numpy as np
# from opencaxpy import TriangleMesh, LagrangeSpace, Field, Model, Problem, PoissonPhysics, SteadyAnalysis


# def src(x):
#     return 2*np.pi**2*np.sin(np.pi*x[0])*np.sin(np.pi*x[1])


# mesh = TriangleMesh.from_box((0, 1, 0, 1), 20, 20)
# problem = Problem(Model(mesh=mesh))
# problem.add_field(Field("u", LagrangeSpace(mesh)))
# r = SteadyAnalysis(problem).solve_poisson("u", PoissonPhysics(1.0, src), 0.0)
# ue = np.sin(np.pi*mesh.points[:, 0])*np.sin(np.pi*mesh.points[:, 1])
# print(ue)
# print("RMS =", np.sqrt(np.mean((r.field("u").values-ue)**2)))
import numpy as np

from opencaxpy import (
    TriangleMesh,
    LagrangeSpace,
    Field,
    Model,
    Problem,
    PoissonPhysics,
    SteadyAnalysis,
)

from opencaxpy.visualization import (
    VTKMeshViewer,
    VTKMeshViewerOptions,
)


def src(x):
    return (
        2.0
        * np.pi**2
        * np.sin(np.pi * x[0])
        * np.sin(np.pi * x[1])
    )


def main():
    # ------------------------------------------------------------
    # 1. Mesh
    # ------------------------------------------------------------
    mesh = TriangleMesh.from_box(
        (0.0, 1.0, 0.0, 1.0),
        50,
        50,
    )

    # ------------------------------------------------------------
    # 2. Problem
    # ------------------------------------------------------------
    problem = Problem(
        Model(mesh=mesh)
    )

    problem.add_field(
        Field(
            "u",
            LagrangeSpace(mesh),
        )
    )

    # ------------------------------------------------------------
    # 3. Solve
    # ------------------------------------------------------------
    result = SteadyAnalysis(problem).solve_poisson(
        "u",
        PoissonPhysics(
            1.0,
            src,
        ),
        0.0,
    )

    # FEM 数值解
    uh = result.field("u").values

    # ------------------------------------------------------------
    # 4. Exact solution
    # ------------------------------------------------------------
    x = mesh.points[:, 0]
    y = mesh.points[:, 1]

    ue = (
        np.sin(np.pi * x)
        * np.sin(np.pi * y)
    )

    # ------------------------------------------------------------
    # 5. Error
    # ------------------------------------------------------------
    error = uh - ue

    rms = np.sqrt(
        np.mean(error**2)
    )

    print("uh =")
    print(uh)

    print()
    print("ue =")
    print(ue)

    print()
    print("RMS =", rms)

    # ------------------------------------------------------------
    # 6. VTK visualization
    # ------------------------------------------------------------
    options = VTKMeshViewerOptions(
        show_surface=True,
        show_edges=False,
        show_nodes=False,

        show_node_ids=False,
        show_edge_ids=False,
        show_face_ids=False,
        show_cell_ids=False,

        title="OpenCAXPy - Poisson FEM Solution",
    )

    viewer = VTKMeshViewer(
        mesh,
        options=options,
    )

    # 将 FEM 解 uh 作为节点标量场
    viewer.add_point_scalar(
        "uh",
        uh,
    )

    viewer.show()


if __name__ == "__main__":
    main()