from __future__ import annotations

from .figure import Figure
from .plot.mesh import MeshPlot
from .plot.solution import SolutionPlot
from .plot.convergence import ConvergencePlot


def show(
    plots,
    *,
    layout=None,
    title=None,
    save_path=None,
    interactive=True,
    options=None,
):
    """显示多个 Plot，并根据 backend 自动选择组合方式。"""

    fig = Figure(
        layout=layout,
        options=options,
        title=title,
    )

    for plot in plots:
        fig.add(plot)

    return fig.show(
        save_path=save_path,
        interactive=interactive,
    )


def show_mesh(
    mesh,
    *,
    style=None,
    title=None,
    layout=None,
    save_path=None,
    interactive=True,
):
    """显示一个或多个网格。

    Parameters
    ----------
    mesh
        单个 Mesh，或 Mesh 序列。
    style : MeshStyle, optional
        网格绘制样式。
    title : str, optional
        单图标题；多网格时作为总标题和子图标题前缀。
    layout : tuple[int, int], optional
        多网格布局，例如 ``(1, 3)``。
    save_path : path-like, optional
        保存路径。
    interactive : bool
        是否显示交互窗口。
    """

    if isinstance(mesh, (list, tuple)):
        plots = [
            MeshPlot(
                item,
                style=style,
                title=None if title is None else f"{title} {i + 1}",
            )
            for i, item in enumerate(mesh)
        ]

        return show(
            plots,
            layout=layout,
            title=title,
            save_path=save_path,
            interactive=interactive,
        )

    return show(
        [
            MeshPlot(
                mesh,
                style=style,
                title=title,
            )
        ],
        layout=(1, 1),
        save_path=save_path,
        interactive=interactive,
    )


def show_solution(
    mesh,
    solution,
    *,
    field=None,
    fields=None,
    component=None,
    deformation=None,
    scale=1.0,
    layout=None,
    title=None,
    save_path=None,
    interactive=True,
    mesh_style=None,
    field_style=None,
    deformation_style=None,
):
    """显示一个或多个数值解 Field。"""

    specs = fields if fields is not None else [field]

    if specs == [None]:
        raise ValueError("field or fields must be provided")

    plots = []

    for spec in specs:
        if isinstance(spec, (tuple, list)):
            name, comp = spec
        else:
            name, comp = spec, component

        plots.append(
            SolutionPlot(
                mesh,
                solution,
                field=name,
                component=comp,
                deformation=deformation,
                scale=scale,
                mesh_style=mesh_style,
                field_style=field_style,
                deformation_style=deformation_style,
                title=name if len(specs) > 1 else title,
            )
        )

    return show(
        plots,
        layout=layout,
        title=title if len(specs) > 1 else None,
        save_path=save_path,
        interactive=interactive,
    )


def show_convergence(
    h,
    error,
    *,
    label="error",
    expected_order=None,
    title="Error convergence",
    save_path=None,
    interactive=True,
):
    """显示误差收敛曲线。"""

    return show(
        [
            ConvergencePlot(
                h,
                error,
                label=label,
                expected_order=expected_order,
                title=title,
            )
        ],
        layout=(1, 1),
        save_path=save_path,
        interactive=interactive,
    )


# v1.x 函数名兼容；新代码推荐使用 show_mesh。
view_mesh = show_mesh
