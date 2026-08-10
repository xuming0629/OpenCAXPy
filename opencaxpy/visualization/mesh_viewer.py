import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from .options import MeshViewerOptions


class MeshViewer:
    def __init__(self, mesh, options=None):
        self.mesh = mesh
        self.options = options or MeshViewerOptions()

    def plot(self, *, ax=None, save_path=None, show=True):
        if self.mesh.geometric_dimension <= 2:
            fig, ax = self._plot_2d(ax)
        else:
            fig, ax = self._plot_3d(ax)

        if save_path is not None:
            fig.savefig(
                save_path,
                dpi=180,
                bbox_inches="tight",
            )

        if show:
            plt.show()

        return fig, ax

    def _plot_2d(self, ax):
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))
        else:
            fig = ax.figure

        points = self.mesh.points

        if points.shape[1] == 1:
            xy = np.column_stack([
                points[:, 0],
                np.zeros(len(points)),
            ])
        else:
            xy = points[:, :2]

        if self.options.show_edges:
            for edge in self.mesh.entity("edge"):
                p = xy[edge]
                ax.plot(
                    p[:,0],
                    p[:,1],
                    linewidth=self.options.line_width,
                )

        if (
            self.options.show_boundary
            and self.mesh.topological_dimension == 2
        ):
            for edge in self.mesh.entity("edge")[
                self.mesh.boundary_edge_index()
            ]:
                p = xy[edge]
                ax.plot(
                    p[:,0],
                    p[:,1],
                    linewidth=2*self.options.line_width,
                )

        if self.options.show_nodes:
            ax.scatter(
                xy[:,0],
                xy[:,1],
                s=self.options.node_size,
            )

        if self.options.show_node_ids:
            for i, p in enumerate(xy):
                ax.text(p[0], p[1], f"N{i}")

        if self.options.show_edge_ids:
            centers = self.mesh.entity_barycenter("edge")
            if centers.shape[1] == 1:
                centers = np.column_stack([
                    centers[:,0],
                    np.zeros(len(centers)),
                ])
            for i, p in enumerate(centers):
                ax.text(p[0], p[1], f"E{i}")

        if self.options.show_cell_ids:
            centers = self.mesh.entity_barycenter("cell")
            for i, p in enumerate(centers):
                y = p[1] if len(p) > 1 else 0.0
                ax.text(p[0], y, f"C{i}")

        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("X")
        if self.mesh.geometric_dimension > 1:
            ax.set_ylabel("Y")
        ax.grid(True, alpha=0.2)
        ax.set_title(
            self.options.title
            or (
                f"{self.mesh.cell_type}: "
                f"{self.mesh.number_of_nodes()} nodes / "
                f"{self.mesh.number_of_cells()} cells"
            )
        )
        fig.tight_layout()
        return fig, ax

    def _plot_3d(self, ax):
        if ax is None:
            fig = plt.figure(figsize=(8, 7))
            ax = fig.add_subplot(111, projection="3d")
        else:
            fig = ax.figure

        points = self.mesh.points

        if self.options.show_edges:
            for edge in self.mesh.entity("edge"):
                p = points[edge]
                ax.plot(
                    p[:,0],
                    p[:,1],
                    p[:,2],
                    linewidth=self.options.line_width,
                )

        if self.options.show_boundary:
            face_ids = self.mesh.boundary_face_index()
            faces = self.mesh.entity("face")[face_ids]
            polygons = [points[face] for face in faces]

            ax.add_collection3d(
                Poly3DCollection(
                    polygons,
                    alpha=self.options.boundary_alpha,
                )
            )

        if self.options.show_nodes:
            ax.scatter(
                points[:,0],
                points[:,1],
                points[:,2],
                s=self.options.node_size,
            )

        if self.options.show_node_ids:
            for i, p in enumerate(points):
                ax.text(p[0], p[1], p[2], f"N{i}")

        if self.options.show_edge_ids:
            centers = self.mesh.entity_barycenter("edge")
            for i, p in enumerate(centers):
                ax.text(p[0], p[1], p[2], f"E{i}")

        if self.options.show_face_ids:
            centers = self.mesh.entity_barycenter("face")
            for i, p in enumerate(centers):
                ax.text(p[0], p[1], p[2], f"F{i}")

        if self.options.show_cell_ids:
            centers = self.mesh.entity_barycenter("cell")
            for i, p in enumerate(centers):
                ax.text(p[0], p[1], p[2], f"C{i}")

        self._set_axes_equal(ax)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title(
            self.options.title
            or (
                f"{self.mesh.cell_type}: "
                f"{self.mesh.number_of_nodes()} nodes / "
                f"{self.mesh.number_of_cells()} cells"
            )
        )
        fig.tight_layout()
        return fig, ax

    def _set_axes_equal(self, ax):
        p = self.mesh.points
        mins = p.min(axis=0)
        maxs = p.max(axis=0)
        center = 0.5*(mins+maxs)
        radius = 0.5*np.max(maxs-mins)
        if radius <= 0:
            radius = 0.5

        ax.set_xlim(center[0]-radius, center[0]+radius)
        ax.set_ylim(center[1]-radius, center[1]+radius)
        ax.set_zlim(center[2]-radius, center[2]+radius)


def plot_mesh(mesh, *, options=None, ax=None, save_path=None, show=True):
    return MeshViewer(
        mesh,
        options=options,
    ).plot(
        ax=ax,
        save_path=save_path,
        show=show,
    )
