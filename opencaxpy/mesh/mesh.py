#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : mesh.py
# @Time          : 2026-08-11 09:52:59
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy 通用网格数据结构及基础几何计算
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from __future__ import annotations

import numpy as np

from .cell_type import get_cell_type
from .topology import MeshTopology


class Mesh:
    """
    OpenCAXPy 通用单一 CellType 网格基类。

    Mesh 是 OpenCAXPy 网格模块中的核心数据结构，主要负责：

        - 节点坐标管理；
        - 单元连接关系管理；
        - CellType 管理；
        - MeshTopology 延迟构建；
        - Node / Edge / Face / Cell 实体访问；
        - 拓扑邻接关系访问；
        - 边界实体查询；
        - 实体重心计算；
        - 边长度计算；
        - 单元面积 / 体积计算；
        - 基础网格质量评估；
        - 网格统计信息汇总。

    当前 Mesh 采用“单一 CellType”设计，即一个 Mesh 对象中只包含
    一种类型的 Cell。

    例如：

        TriangleMesh:
            所有 Cell 都是 triangle3

        TetrahedronMesh:
            所有 Cell 都是 tetra4

    混合网格后续可以单独设计 MixedMesh，而不建议直接让 Mesh 同时
    承担单一网格和混合网格两种职责。

    Notes
    -----
    Mesh 负责“几何数据 + 用户 API”。

    MeshTopology 负责：

        - 全局 Edge 构建；
        - 全局 Face 构建；
        - Cell -> Edge；
        - Cell -> Face；
        - Edge -> Cell；
        - Face -> Cell；
        - Boundary Node；
        - Boundary Edge；
        - Boundary Face。

    Mesh 不负责：

        - 网格生成算法；
        - 外部网格导入；
        - FEM 形函数；
        - 数值积分；
        - 求解器；
        - VTK 可视化。

    对应职责分别属于：

        mesh/generators/
            网格生成

        mesh/adapters/
            Gmsh / meshio 等外部网格转换

        discretization/
            FEM / FVM / FDM

        visualization/
            VTK 可视化
    """

    def __init__(
        self,
        points,
        cells,
        cell_type,
    ):
        """
        初始化 Mesh。

        Parameters
        ----------
        points : array_like
            网格节点坐标。

            标准 shape：

                (NN, GD)

            其中：

                NN:
                    Number of Nodes

                GD:
                    Geometric Dimension

            当前支持：

                GD = 1
                GD = 2
                GD = 3

        cells : array_like
            单元连接关系。

            shape：

                (NC, NVC)

            其中：

                NC:
                    Number of Cells

                NVC:
                    Number of Vertices per Cell

        cell_type : str
            OpenCAXPy 标准 CellType 名称，例如：

                "line2"
                "triangle3"
                "quad4"
                "tetra4"
                "hexa8"
        """

        # ============================================================
        # 1. 标准化基础网格数据
        # ============================================================

        # 节点坐标统一转换为 float NumPy 数组。
        self.points = np.asarray(
            points,
            dtype=float,
        )

        # Cell connectivity 统一转换为整数 NumPy 数组。
        self.cells = np.asarray(
            cells,
            dtype=int,
        )

        # CellType 名称统一转换为小写。
        self.cell_type = str(cell_type).lower()

        # 获取当前 CellType 的标准描述对象。
        #
        # descriptor 中包含：
        #
        #     name
        #     dimension
        #     num_nodes
        #     local_edges
        #     local_faces
        #
        desc = get_cell_type(self.cell_type)

        # ============================================================
        # 2. 节点数据合法性检查
        # ============================================================

        # OpenCAXPy Mesh 统一要求：
        #
        #     points.shape == (NN, GD)
        #
        # 因此必须是二维数组。
        if self.points.ndim != 2:
            raise ValueError("points must have shape (NN, GD)")

        # 当前只支持 1D / 2D / 3D 几何空间。
        if self.points.shape[1] not in (
            1,
            2,
            3,
        ):
            raise ValueError("geometric dimension must be 1, 2, or 3")

        # ============================================================
        # 3. Cell connectivity 合法性检查
        # ============================================================

        # cells 必须是二维连接矩阵。
        #
        # 同时每个 Cell 的节点数量必须和 CellType 描述一致。
        #
        # 例如：
        #
        #     triangle3:
        #         cells.shape[1] == 3
        #
        #     hexa8:
        #         cells.shape[1] == 8
        #
        if self.cells.ndim != 2 or self.cells.shape[1] != desc.num_nodes:
            raise ValueError(
                f"{self.cell_type!r} expects "
                f"{desc.num_nodes} nodes per cell, "
                f"but got cells shape {self.cells.shape}"
            )

        # 如果存在 Cell，则检查节点编号是否合法。
        if self.cells.size:

            # Node ID 不能为负数。
            if self.cells.min() < 0:
                raise ValueError("cell connectivity contains negative node index")

            # 最大 Node ID 不能超过 points 数组范围。
            if self.cells.max() >= len(self.points):
                raise ValueError("cell connectivity contains invalid node index")

        # ============================================================
        # 4. MeshTopology 延迟缓存
        # ============================================================

        # 拓扑信息不在 Mesh 初始化时立即生成。
        #
        # 当第一次访问：
        #
        #     mesh.topology
        #
        # 或：
        #
        #     mesh.number_of_edges()
        #
        # 等需要拓扑信息的方法时才真正构建。
        #
        # 这样可以避免只使用 points / cells 时产生不必要计算。
        self._topology = None

    # ================================================================
    # CellType / Topology 属性
    # ================================================================

    @property
    def descriptor(self):
        """
        获取当前 Mesh 的 CellType 描述对象。

        Returns
        -------
        CellType
            当前 CellType 的标准描述。
        """
        return get_cell_type(self.cell_type)

    @property
    def topology(self):
        """
        获取 MeshTopology。

        采用延迟初始化策略。

        Returns
        -------
        MeshTopology
            当前网格拓扑对象。
        """

        if self._topology is None:
            self._topology = MeshTopology(
                self.cells,
                self.cell_type,
            )

        return self._topology

    # ================================================================
    # 几何维度 / 拓扑维度
    # ================================================================

    @property
    def geometric_dimension(self):
        """
        返回几何维度 GD。

        Examples
        --------
        一维 Line Mesh：

            GD = 1

        二维平面 Triangle Mesh：

            GD = 2

        三维空间中的 Triangle Surface Mesh：

            GD = 3

        Returns
        -------
        int
            几何维度。
        """
        return self.points.shape[1]

    @property
    def topological_dimension(self):
        """
        返回拓扑维度 TD。

        Examples
        --------
        line2:

            TD = 1

        triangle3 / quad4:

            TD = 2

        tetra4 / hexa8:

            TD = 3

        Returns
        -------
        int
            网格拓扑维度。
        """
        return self.descriptor.dimension

    # ================================================================
    # 网格实体数量
    # ================================================================

    def number_of_nodes(self):
        """
        返回全局节点数量。

        Returns
        -------
        int
            Number of Nodes。
        """
        return len(self.points)

    def number_of_edges(self):
        """
        返回全局唯一 Edge 数量。

        Edge 由 MeshTopology 根据各 Cell 的 local_edges
        自动合并生成。

        Returns
        -------
        int
            Number of Edges。
        """
        return len(self.topology.edges)

    def number_of_faces(self):
        """
        返回 Face 数量。

        规则：

            TD < 2:
                没有 Face，返回 0。

            TD == 2:
                Cell 本身就是二维 Face，
                因此返回 Cell 数量。

            TD == 3:
                返回 MeshTopology 中的全局唯一 Face 数量。

        Returns
        -------
        int
            Number of Faces。
        """

        if self.topological_dimension < 2:
            return 0

        if self.topological_dimension == 2:
            return self.number_of_cells()

        return len(self.topology.faces)

    def number_of_cells(self):
        """
        返回 Cell 数量。

        Returns
        -------
        int
            Number of Cells。
        """
        return len(self.cells)

    # ================================================================
    # 实体访问
    # ================================================================

    def entity(
        self,
        entity_type,
    ):
        """
        获取指定类型的网格实体。

        Parameters
        ----------
        entity_type : str | int
            支持字符串：

                "node"
                "point"
                "vertex"
                "edge"
                "face"
                "cell"

            也支持拓扑维度：

                0 -> Node
                1 -> Edge
                2 -> Face / 2D Cell
                3 -> Cell

        Returns
        -------
        numpy.ndarray
            对应网格实体。

        Notes
        -----
        对二维网格：

            face == cell

        因此：

            mesh.entity("face")

        返回二维 Cell connectivity。
        """

        # ------------------------------------------------------------
        # 通过拓扑维度访问实体
        # ------------------------------------------------------------

        if isinstance(
            entity_type,
            int,
        ):
            mapping = {
                0: "node",
                1: "edge",
                2: ("cell" if self.topological_dimension == 2 else "face"),
                3: "cell",
            }

            if entity_type not in mapping:
                raise ValueError(f"Unsupported entity dimension: {entity_type}")

            entity_type = mapping[entity_type]

        # 字符串统一转为小写。
        entity_type = str(entity_type).lower()

        # ------------------------------------------------------------
        # Node / Point / Vertex
        # ------------------------------------------------------------

        if entity_type in (
            "node",
            "point",
            "vertex",
        ):
            return self.points

        # ------------------------------------------------------------
        # Edge
        # ------------------------------------------------------------

        if entity_type == "edge":
            return self.topology.edges

        # ------------------------------------------------------------
        # Face
        # ------------------------------------------------------------

        if entity_type == "face":

            # 对于 2D Mesh：
            #
            #     Cell == Face
            #
            if self.topological_dimension == 2:
                return self.cells

            return self.topology.faces

        # ------------------------------------------------------------
        # Cell
        # ------------------------------------------------------------

        if entity_type == "cell":
            return self.cells

        raise ValueError(f"Unsupported entity type: {entity_type!r}")

    def cell_coordinates(
        self,
        i,
    ):
        """
        获取指定 Cell 的节点坐标。

        Parameters
        ----------
        i : int
            全局 Cell ID。

        Returns
        -------
        numpy.ndarray
            当前 Cell 的全部节点坐标。

        Examples
        --------
        Triangle3：

            shape = (3, GD)

        Hexa8：

            shape = (8, 3)
        """
        return self.points[self.cells[i]]

    # ================================================================
    # Topology 邻接关系
    # ================================================================

    def cell_to_edge(self):
        """
        获取 Cell -> Edge 映射。

        Returns
        -------
        numpy.ndarray
            每个 Cell 的局部 Edge 对应的全局 Edge ID。
        """
        return self.topology.cell_to_edge()

    def cell_to_face(self):
        """
        获取 Cell -> Face 映射。

        对二维网格：

            每个 Cell 本身就是一个 Face。

        因此：

            cell i -> face i

        Returns
        -------
        numpy.ndarray
            Cell 到 Face 的映射。
        """

        if self.topological_dimension == 2:
            return np.arange(
                self.number_of_cells(),
                dtype=int,
            )[:, None]

        return self.topology.cell_to_face()

    def edge_to_cell(self):
        """
        获取 Edge -> Cell 邻接关系。

        Returns
        -------
        tuple
            每条 Edge 相邻的 Cell ID。
        """
        return self.topology.edge_to_cell()

    def face_to_cell(self):
        """
        获取 Face -> Cell 邻接关系。

        对二维网格：

            Face 本身就是 Cell。

        Returns
        -------
        tuple
            每个 Face 相邻的 Cell ID。
        """

        if self.topological_dimension == 2:
            return tuple((i,) for i in range(self.number_of_cells()))

        return self.topology.face_to_cell()

    # ================================================================
    # 边界实体
    # ================================================================

    def boundary_node_index(self):
        """
        返回边界节点编号。

        Returns
        -------
        numpy.ndarray
            Boundary Node ID。
        """
        return self.topology.boundary_node_index()

    def boundary_edge_index(self):
        """
        返回边界 Edge 编号。

        Returns
        -------
        numpy.ndarray
            Boundary Edge ID。
        """
        return self.topology.boundary_edge_index()

    def boundary_face_index(self):
        """
        返回边界 Face 编号。

        Notes
        -----
        对二维网格：

            每个二维 Cell 本身都是 Face，
            因此当前返回所有 Cell ID。

        对三维网格：

            返回只属于一个 Cell 的外边界 Face。

        Returns
        -------
        numpy.ndarray
            Boundary Face ID。
        """

        if self.topological_dimension == 2:
            return np.arange(
                self.number_of_cells(),
                dtype=int,
            )

        return self.topology.boundary_face_index()

    def boundary_facet_index(self):
        """
        返回 codimension-1 边界实体编号。

        Facet 是有限元和 PDE 离散中非常重要的统一概念。

        对不同拓扑维度：

            TD = 1:
                Facet = Node

            TD = 2:
                Facet = Edge

            TD = 3:
                Facet = Face

        Returns
        -------
        numpy.ndarray
            边界 Facet ID。

        Examples
        --------
        2D Triangle Mesh：

            boundary_facet_index()
                == boundary_edge_index()

        3D Tetra Mesh：

            boundary_facet_index()
                == boundary_face_index()
        """

        if self.topological_dimension == 1:
            return self.boundary_node_index()

        if self.topological_dimension == 2:
            return self.boundary_edge_index()

        if self.topological_dimension == 3:
            return self.boundary_face_index()

        raise NotImplementedError(self.topological_dimension)

    # ================================================================
    # 实体几何
    # ================================================================

    def entity_barycenter(
        self,
        entity_type="cell",
    ):
        """
        计算指定实体的重心。

        Parameters
        ----------
        entity_type : str | int
            实体类型。

        Returns
        -------
        numpy.ndarray
            实体重心坐标。

        Notes
        -----
        对 Node：

            重心就是节点本身。

        对 Edge / Face / Cell：

            当前使用所有节点坐标的算术平均值。
        """

        if entity_type in (
            "node",
            "point",
            "vertex",
            0,
        ):
            return self.points.copy()

        entity = self.entity(entity_type)

        return self.points[entity].mean(axis=1)

    def edge_length(self):
        """
        计算所有全局 Edge 的几何长度。

        Returns
        -------
        numpy.ndarray
            每条 Edge 的长度。
        """

        edge = self.entity("edge")

        if edge.size == 0:
            return np.empty(
                0,
                dtype=float,
            )

        # 每条 Edge 两端节点坐标：
        #
        #     shape = (NE, 2, GD)
        #
        p = self.points[edge]

        return np.linalg.norm(
            p[:, 1] - p[:, 0],
            axis=1,
        )

    # ================================================================
    # 基础几何测度
    # ================================================================

    @staticmethod
    def _triangle_area(
        tri,
    ):
        """
        计算 Triangle3 面积。

        支持：

            - 二维平面 Triangle；
            - 三维空间 Triangle Surface。

        Parameters
        ----------
        tri : numpy.ndarray
            Triangle 坐标。

            shape：

                (NT, 3, GD)

        Returns
        -------
        numpy.ndarray
            每个 Triangle 的面积。
        """

        # 两条边向量。
        a = tri[:, 1] - tri[:, 0]

        b = tri[:, 2] - tri[:, 0]

        # ------------------------------------------------------------
        # 2D Triangle
        # ------------------------------------------------------------

        if tri.shape[-1] == 2:

            # 使用二维叉积标量：
            #
            #     A = 1 / 2 * |ax * by - ay * bx|
            #
            return 0.5 * np.abs(a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0])

        # ------------------------------------------------------------
        # 3D Triangle Surface
        # ------------------------------------------------------------

        if tri.shape[-1] == 3:

            # 三维叉积：
            #
            #     A = 1 / 2 * ||a × b||
            #
            return 0.5 * np.linalg.norm(
                np.cross(
                    a,
                    b,
                ),
                axis=1,
            )

        raise ValueError("triangle area requires " "geometric dimension 2 or 3")

    @staticmethod
    def _tetra_volume(
        tet,
    ):
        """
        计算 Tetra4 体积。

        Parameters
        ----------
        tet : numpy.ndarray
            Tetra4 节点坐标。

            shape：

                (NT, 4, 3)

        Returns
        -------
        numpy.ndarray
            每个 Tetra4 的体积。
        """

        if tet.shape[-1] != 3:
            raise ValueError("tetrahedron volume requires " "geometric dimension 3")

        # 三条从 vertex 0 出发的边向量。
        a = tet[:, 1] - tet[:, 0]

        b = tet[:, 2] - tet[:, 0]

        c = tet[:, 3] - tet[:, 0]

        # 四面体体积：
        #
        #     V = |(a × b) · c| / 6
        #
        return (
            np.abs(
                np.einsum(
                    "ij,ij->i",
                    np.cross(
                        a,
                        b,
                    ),
                    c,
                )
            )
            / 6.0
        )

    def entity_measure(
        self,
        entity_type="cell",
    ):
        """
        计算实体几何测度。

        当前支持：

            Edge:
                长度

            Line2 Cell:
                长度

            Triangle3 Cell:
                面积

            Quad4 Cell:
                面积

            Tetra4 Cell:
                体积

            Hexa8 Cell:
                体积

        Parameters
        ----------
        entity_type : str
            当前支持：

                "edge"
                "cell"

        Returns
        -------
        numpy.ndarray
            对应实体的长度 / 面积 / 体积。
        """

        # ------------------------------------------------------------
        # Edge
        # ------------------------------------------------------------

        if entity_type == "edge":
            return self.edge_length()

        # 当前除 Cell 外暂未统一实现 Face measure。
        if entity_type != "cell":
            raise NotImplementedError(entity_type)

        # Cell 所有节点坐标：
        #
        #     shape =
        #         (NC, num_nodes_per_cell, GD)
        #
        x = self.points[self.cells]

        # ------------------------------------------------------------
        # Line2
        # ------------------------------------------------------------

        if self.cell_type == "line2":
            return np.linalg.norm(
                x[:, 1] - x[:, 0],
                axis=1,
            )

        # ------------------------------------------------------------
        # Triangle3
        # ------------------------------------------------------------

        if self.cell_type == "triangle3":
            return self._triangle_area(x)

        # ------------------------------------------------------------
        # Quad4
        # ------------------------------------------------------------

        if self.cell_type == "quad4":

            # 当前通过对角线：
            #
            #     0 -> 2
            #
            # 将 Quad4 拆分为：
            #
            #     triangle 0:
            #         (0, 1, 2)
            #
            #     triangle 1:
            #         (0, 2, 3)
            #
            return self._triangle_area(x[:, [0, 1, 2]]) + self._triangle_area(x[:, [0, 2, 3]])

        # ------------------------------------------------------------
        # Tetra4
        # ------------------------------------------------------------

        if self.cell_type == "tetra4":
            return self._tetra_volume(x)

        # ------------------------------------------------------------
        # Hexa8
        # ------------------------------------------------------------

        if self.cell_type == "hexa8":

            # 将 Hexa8 分解成 5 个 Tetra4，
            # 用于当前基础几何体积计算。
            #
            # 注意：
            #
            # FEM 中真正的 Hexa8 数值积分不应该使用该方法，
            # 而应该使用参考单元 + Jacobian + Gaussian Quadrature。
            #
            tet_ids = (
                (0, 1, 3, 4),
                (1, 2, 3, 6),
                (1, 3, 4, 6),
                (1, 4, 5, 6),
                (3, 4, 6, 7),
            )

            volume = np.zeros(
                self.number_of_cells(),
                dtype=float,
            )

            for ids in tet_ids:
                volume += self._tetra_volume(x[:, ids])

            return volume

        raise NotImplementedError(self.cell_type)

    # ================================================================
    # 网格质量
    # ================================================================

    def cell_quality(self):
        """
        计算每个 Cell 的基础网格质量指标。

        当前实现：

            Line2:
                q = 1

            Triangle3:
                Mean-ratio 类质量指标

            Tetra4:
                基于体积与边长的质量指标

            Quad4:
                min(edge length) / max(edge length)

            Hexa8:
                min(edge length) / max(edge length)

        Returns
        -------
        numpy.ndarray
            每个 Cell 的质量指标。

        Notes
        -----
        当前 Quad4 / Hexa8 使用的是非常基础的边长比例指标，
        主要用于轻量级网格诊断。

        后续建议继续增加：

            - Aspect Ratio
            - Scaled Jacobian
            - Jacobian Determinant
            - Skewness
            - Warpage
            - Condition Number
        """

        x = self.points[self.cells]

        # ------------------------------------------------------------
        # Line2
        # ------------------------------------------------------------

        if self.cell_type == "line2":
            return np.ones(
                self.number_of_cells(),
                dtype=float,
            )

        # ------------------------------------------------------------
        # Triangle3
        # ------------------------------------------------------------

        if self.cell_type == "triangle3":

            # 三条边长度平方之和。
            e2 = (
                np.sum(
                    (x[:, 1] - x[:, 0]) ** 2,
                    axis=1,
                )
                + np.sum(
                    (x[:, 2] - x[:, 1]) ** 2,
                    axis=1,
                )
                + np.sum(
                    (x[:, 0] - x[:, 2]) ** 2,
                    axis=1,
                )
            )

            area = self.entity_measure("cell")

            # Triangle mean-ratio 类指标：
            #
            #            4 sqrt(3) A
            #     q = -----------------
            #           l1²+l2²+l3²
            #
            # 正三角形：
            #
            #     q = 1
            #
            with np.errstate(
                divide="ignore",
                invalid="ignore",
            ):
                q = 4.0 * np.sqrt(3.0) * area / e2

            return np.nan_to_num(q)

        # ------------------------------------------------------------
        # Tetra4
        # ------------------------------------------------------------

        if self.cell_type == "tetra4":

            # 六条 Edge 长度平方和。
            l2 = np.zeros(
                self.number_of_cells(),
                dtype=float,
            )

            for a, b in self.descriptor.local_edges:
                l2 += np.sum(
                    (x[:, a] - x[:, b]) ** 2,
                    axis=1,
                )

            volume = self.entity_measure("cell")

            # 基于体积 / 边长的 Tetra 质量指标。
            with np.errstate(
                divide="ignore",
                invalid="ignore",
            ):
                q = (
                    12.0
                    * np.power(
                        3.0 * volume,
                        2.0 / 3.0,
                    )
                    / l2
                )

            return np.nan_to_num(q)

        # ------------------------------------------------------------
        # Quad4 / Hexa8
        # ------------------------------------------------------------

        if self.cell_type in (
            "quad4",
            "hexa8",
        ):

            # 获取每个 Cell 对应的所有局部 Edge 长度。
            #
            # edge_length():
            #     全局 Edge 长度
            #
            # cell_to_edge():
            #     Cell -> global Edge ID
            #
            lengths = self.edge_length()[self.cell_to_edge()]

            # 最短边 / 最长边。
            #
            # 理想规则单元：
            #
            #     q = 1
            #
            with np.errstate(
                divide="ignore",
                invalid="ignore",
            ):
                q = lengths.min(axis=1) / lengths.max(axis=1)

            return np.nan_to_num(q)

        raise NotImplementedError(self.cell_type)

    # ================================================================
    # 网格统计摘要
    # ================================================================

    def summary(self):
        """
        返回网格基础统计信息。

        Returns
        -------
        dict
            网格摘要信息。

        返回内容包括：

            cell_type
            geometric_dimension
            topological_dimension

            num_nodes
            num_edges
            num_faces
            num_cells

            num_boundary_nodes
            num_boundary_edges
            num_boundary_faces

            measure_sum

            quality_min
            quality_mean
        """

        # 计算网格质量。
        quality = self.cell_quality()

        # 计算 Cell 几何测度。
        measure = self.entity_measure("cell")

        return {
            # --------------------------------------------------------
            # 基础类型
            # --------------------------------------------------------
            "cell_type": self.cell_type,
            "geometric_dimension": self.geometric_dimension,
            "topological_dimension": self.topological_dimension,
            # --------------------------------------------------------
            # 实体数量
            # --------------------------------------------------------
            "num_nodes": self.number_of_nodes(),
            "num_edges": self.number_of_edges(),
            "num_faces": self.number_of_faces(),
            "num_cells": self.number_of_cells(),
            # --------------------------------------------------------
            # 边界实体数量
            # --------------------------------------------------------
            "num_boundary_nodes": len(self.boundary_node_index()),
            "num_boundary_edges": len(self.boundary_edge_index()),
            "num_boundary_faces": len(self.boundary_face_index()),
            # --------------------------------------------------------
            # 几何测度
            # --------------------------------------------------------
            "measure_sum": (float(measure.sum()) if measure.size else 0.0),
            # --------------------------------------------------------
            # 网格质量
            # --------------------------------------------------------
            "quality_min": (float(quality.min()) if quality.size else None),
            "quality_mean": (float(quality.mean()) if quality.size else None),
        }
