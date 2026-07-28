from __future__ import annotations

import numpy as np

from .options import PlotOptions


def _to_numpy(mesh, value):
    return mesh.backend.to_numpy(value)


def _text(axes, x, y, value, *, color, size):
    axes.text(
        x,
        y,
        str(value),
        color=color,
        fontsize=size,
        horizontalalignment="center",
        verticalalignment="center",
        zorder=5,
    )


def plot_mesh(
    mesh,
    *,
    axes=None,
    options: PlotOptions | None = None,
    **kwargs,
):
    try:
        import matplotlib.pyplot as plt
        import matplotlib.tri as mtri
        from matplotlib.collections import PolyCollection
    except ImportError as exc:
        raise ImportError(
            "Matplotlib plotting requires `pip install opencaxpy[plot]`"
        ) from exc

    options = options or PlotOptions(**kwargs)

    points = _to_numpy(mesh, mesh.points)
    cells = _to_numpy(mesh, mesh.cells)
    corners = np.asarray(mesh.cell_type.corner_nodes, dtype=np.int64)
    corner_cells = cells[:, corners]

    if points.shape[1] < 2:
        raise ValueError("plot_mesh requires at least two coordinate dimensions")

    if axes is None:
        _, axes = plt.subplots()

    axes.set_facecolor(options.background_color)

    scalar = None
    if options.scalar_name:
        source = (
            mesh.point_data
            if options.scalar_location == "point"
            else mesh.cell_data
        )
        if options.scalar_name not in source:
            raise KeyError(
                f"scalar field {options.scalar_name!r} not found in "
                f"{options.scalar_location}_data"
            )
        scalar = _to_numpy(mesh, source[options.scalar_name])

    family = mesh.cell_type.family

    if family == "triangle":
        triangulation = mtri.Triangulation(
            points[:, 0],
            points[:, 1],
            corner_cells[:, :3],
        )

        if scalar is not None:
            if options.scalar_location == "point":
                artist = axes.tripcolor(
                    triangulation,
                    scalar,
                    shading="gouraud",
                    cmap=options.cmap,
                )
            else:
                artist = axes.tripcolor(
                    triangulation,
                    facecolors=scalar,
                    shading="flat",
                    cmap=options.cmap,
                )
            if options.show_scalar_bar:
                plt.colorbar(artist, ax=axes)
        else:
            polygons = points[corner_cells[:, :3], :2]
            collection = PolyCollection(
                polygons,
                facecolors=[options.surface_color],
                edgecolors="none",
            )
            axes.add_collection(collection)

        if options.show_edges:
            axes.triplot(
                triangulation,
                linewidth=options.edge_width,
                color=options.edge_color,
            )

    elif family == "quad":
        polygons = points[corner_cells[:, :4], :2]
        collection = PolyCollection(
            polygons,
            edgecolors=(
                options.edge_color if options.show_edges else "none"
            ),
            linewidths=options.edge_width,
            facecolors=(
                None if scalar is not None else [options.surface_color]
            ),
            cmap=options.cmap,
        )
        if scalar is not None and options.scalar_location == "cell":
            collection.set_array(np.asarray(scalar))
        axes.add_collection(collection)
        axes.autoscale_view()
        if scalar is not None and options.show_scalar_bar:
            plt.colorbar(collection, ax=axes)

    else:
        raise NotImplementedError(
            "Matplotlib plot currently supports triangle and quad meshes"
        )

    if options.show_boundary:
        boundary = _to_numpy(mesh, mesh.boundary_entities("edge"))
        for a, b in boundary:
            p = points[[a, b]]
            axes.plot(
                p[:, 0],
                p[:, 1],
                linewidth=options.boundary_width,
                color=options.boundary_color,
                zorder=4,
            )

    if options.show_nodes:
        axes.scatter(
            points[:, 0],
            points[:, 1],
            s=options.node_size,
            color=options.node_color,
            zorder=4,
        )

    if options.show_node_ids:
        for node_id, point in enumerate(points):
            _text(
                axes,
                point[0],
                point[1],
                node_id,
                color=options.node_label_color,
                size=options.node_label_font_size,
            )

    if options.show_cell_ids:
        centers = _to_numpy(
            mesh,
            mesh.entity_barycenter("cell"),
        )
        for cell_id, center in enumerate(centers):
            _text(
                axes,
                center[0],
                center[1],
                cell_id,
                color=options.cell_label_color,
                size=options.cell_label_font_size,
            )

    if options.show_edge_ids:
        edges = _to_numpy(mesh, mesh.entity("edge"))
        centers = points[edges].mean(axis=1)
        for edge_id, center in enumerate(centers):
            _text(
                axes,
                center[0],
                center[1],
                edge_id,
                color=options.edge_label_color,
                size=options.edge_label_font_size,
            )

    if options.equal_aspect:
        axes.set_aspect("equal", adjustable="box")

    if options.title:
        axes.set_title(options.title)

    if options.show:
        plt.show()

    return axes
