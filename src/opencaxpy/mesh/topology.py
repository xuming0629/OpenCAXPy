from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .connectivity import Connectivity


@dataclass(slots=True)
class Topology:
    mesh: object
    _cache: dict[tuple[str, str], Connectivity] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )
    _entities: dict[str, object] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )
    _orientations: dict[tuple[str, str], object] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    @property
    def backend(self):
        return self.mesh.backend

    @property
    def device(self):
        return self.mesh.device

    def clear(self) -> None:
        self._cache.clear()
        self._entities.clear()
        self._orientations.clear()

    def entities(self, entity: str):
        if entity == "node":
            return self.mesh.points

        if entity == "cell":
            return self.mesh.cells

        if entity == "edge":
            self._ensure_edges()
            return self._entities["edge"]

        raise KeyError(f"unsupported entity type {entity!r}")

    def number_of_entities(self, entity: str) -> int:
        return int(self.entities(entity).shape[0])

    def connectivity(
        self,
        source: str,
        target: str,
    ) -> Connectivity:
        key = (source, target)

        if key in self._cache:
            return self._cache[key]

        if key == ("cell", "node"):
            result = Connectivity.from_dense(
                self.mesh.cells,
                source_name="cell",
                target_name="node",
                target_size=self.mesh.num_nodes,
                backend=self.backend,
                device=self.device,
            )
        elif key in {
            ("cell", "edge"),
            ("edge", "cell"),
            ("node", "cell"),
            ("cell", "cell"),
        }:
            self._ensure_edges()
            result = self._cache[key]
        else:
            raise KeyError(
                f"unsupported connectivity {source!r}->{target!r}"
            )

        self._cache[key] = result
        return result


    def orientation(self, source: str, target: str):
        """Return local-to-global orientation signs.

        Currently ``cell -> edge`` is supported.  A value of ``+1``
        means the directed local edge has the same orientation as the
        canonical global edge; ``-1`` means the orientation is reversed.
        The columns preserve local-edge numbering and are never sorted.
        """
        if (source, target) != ("cell", "edge"):
            raise KeyError(
                f"unsupported orientation {source!r}->{target!r}"
            )
        self._ensure_edges()
        return self._orientations[("cell", "edge")]

    def cell_to_edge_sign(self):
        return self.orientation("cell", "edge")

    def local_edge_nodes(self):
        """Return directed edge-node IDs for every cell/local edge.

        Shape is ``(num_cells, num_local_edges, 2)``.  This array keeps
        the cell-local direction, unlike the canonical global edge table.
        """
        descriptor = self.mesh.cell_type
        local_edges = descriptor.edge_corner_nodes()
        cells_np = self.backend.to_numpy(self.mesh.cells)
        values = [
            [
                (int(cell[local_a]), int(cell[local_b]))
                for local_a, local_b in local_edges
            ]
            for cell in cells_np
        ]
        return self.backend.asarray(
            values,
            dtype=self.backend.dtype_int(),
            device=self.device,
        )

    def boundary_entity_ids(self, entity: str):
        if entity != "edge":
            raise KeyError(
                "v1.0 currently supports boundary edge queries"
            )

        edge_to_cell = self.connectivity("edge", "cell")
        boundary = [
            edge_id
            for edge_id, cells in enumerate(edge_to_cell.to_lists())
            if len(cells) == 1
        ]

        return self.backend.asarray(
            boundary,
            dtype=self.backend.dtype_int(),
            device=self.device,
        )

    def boundary_entities(self, entity: str):
        ids = self.boundary_entity_ids(entity)
        return self.entities(entity)[ids]

    def _ensure_edges(self) -> None:
        if "edge" in self._entities:
            return

        descriptor = self.mesh.cell_type
        local_edges = descriptor.edge_corner_nodes()
        discovery_edges = descriptor.edge_discovery_order
        cells_np = self.backend.to_numpy(self.mesh.cells)

        edge_map: dict[tuple[int, int], int] = {}
        edges: list[tuple[int, int]] = []
        edge_to_cell_rows: list[list[int]] = []

        # Pass 1: discover and number global edges independently from the
        # semantic local-edge numbering used by cell2edge.
        for cell in cells_np:
            for local_a, local_b in discovery_edges:
                a = int(cell[local_a])
                b = int(cell[local_b])
                key = (a, b) if a < b else (b, a)

                if key not in edge_map:
                    edge_map[key] = len(edges)
                    edges.append(key)
                    edge_to_cell_rows.append([])

        cell_to_edge_rows: list[list[int]] = []
        cell_to_edge_sign_rows: list[list[int]] = []
        node_to_cell_rows: list[list[int]] = [
            [] for _ in range(self.mesh.num_nodes)
        ]

        # Pass 2: populate cell2edge in local-edge column order.  For
        # triangles, column i is the edge opposite local node i.
        for cell_id, cell in enumerate(cells_np):
            for node_id in descriptor.corner_nodes:
                node_to_cell_rows[int(cell[node_id])].append(cell_id)

            local_row: list[int] = []
            local_sign_row: list[int] = []

            for local_a, local_b in local_edges:
                a = int(cell[local_a])
                b = int(cell[local_b])
                key = (a, b) if a < b else (b, a)
                edge_id = edge_map[key]

                local_row.append(edge_id)
                local_sign_row.append(1 if (a, b) == key else -1)

                attached = edge_to_cell_rows[edge_id]
                if not attached or attached[-1] != cell_id:
                    attached.append(cell_id)

            cell_to_edge_rows.append(local_row)
            cell_to_edge_sign_rows.append(local_sign_row)

        cell_to_cell_sets = [
            set() for _ in range(self.mesh.num_cells)
        ]

        for attached_cells in edge_to_cell_rows:
            for left_index, left in enumerate(attached_cells):
                for right in attached_cells[left_index + 1 :]:
                    cell_to_cell_sets[left].add(right)
                    cell_to_cell_sets[right].add(left)

        self._entities["edge"] = self.backend.asarray(
            edges,
            dtype=self.backend.dtype_int(),
            device=self.device,
        )

        self._cache[("cell", "edge")] = Connectivity.from_lists(
            cell_to_edge_rows,
            source_name="cell",
            target_name="edge",
            target_size=len(edges),
            backend=self.backend,
            device=self.device,
        )

        self._orientations[("cell", "edge")] = self.backend.asarray(
            cell_to_edge_sign_rows,
            dtype=self.backend.dtype_int(),
            device=self.device,
        )

        self._cache[("edge", "cell")] = Connectivity.from_lists(
            edge_to_cell_rows,
            source_name="edge",
            target_name="cell",
            target_size=self.mesh.num_cells,
            backend=self.backend,
            device=self.device,
        )

        self._cache[("node", "cell")] = Connectivity.from_lists(
            node_to_cell_rows,
            source_name="node",
            target_name="cell",
            target_size=self.mesh.num_cells,
            backend=self.backend,
            device=self.device,
        )

        self._cache[("cell", "cell")] = Connectivity.from_lists(
            [sorted(values) for values in cell_to_cell_sets],
            source_name="cell",
            target_name="cell",
            target_size=self.mesh.num_cells,
            backend=self.backend,
            device=self.device,
        )

    def high_order_edge_nodes(self):
        descriptor = self.mesh.cell_type
        internal = descriptor.edge_internal_nodes()

        if not any(internal):
            return None

        self._ensure_edges()
        cell_to_edge = self.connectivity("cell", "edge")
        cells_np = self.backend.to_numpy(self.mesh.cells)
        c2e = cell_to_edge.to_lists()

        rows: list[list[int] | None] = [
            None for _ in range(self.number_of_entities("edge"))
        ]

        signs = self.backend.to_numpy(
            self.cell_to_edge_sign()
        )

        for cell_id, cell in enumerate(cells_np):
            for local_edge_id, local_internal in enumerate(internal):
                edge_id = c2e[cell_id][local_edge_id]
                values = [int(cell[index]) for index in local_internal]

                # Normalize high-order edge nodes to the canonical global
                # edge direction.  This matters when an adjacent cell uses
                # the shared edge in the opposite local direction.
                if int(signs[cell_id, local_edge_id]) < 0:
                    values.reverse()

                if rows[edge_id] is None:
                    rows[edge_id] = values
                elif rows[edge_id] != values:
                    raise ValueError(
                        "inconsistent high-order nodes on shared edge "
                        f"{edge_id}: {rows[edge_id]} != {values}"
                    )

        normalized = [
            values if values is not None else []
            for values in rows
        ]

        return Connectivity.from_lists(
            normalized,
            source_name="edge",
            target_name="node",
            target_size=self.mesh.num_nodes,
            backend=self.backend,
            device=self.device,
        )
