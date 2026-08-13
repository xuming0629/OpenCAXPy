import numpy as np


class StructuralModel:
    """结构力学高层模型。

    StructuralModel 用于组织结构分析所需的基础计算数据，包括：

    - 节点坐标；
    - 节点自由度数量；
    - 有限元单元；
    - 节点载荷；
    - 位移边界条件。

    当前版本假设所有节点具有相同数量的自由度，
    适用于桁架、梁、平面结构等基础结构有限元分析。
    """

    def __init__(self, points, dofs_per_node):
        # 节点坐标。
        #
        # points 通常为二维数组：
        #
        #     [
        #         [x0, y0],
        #         [x1, y1],
        #         ...
        #     ]
        #
        # 三维模型则可以为：
        #
        #     [
        #         [x0, y0, z0],
        #         [x1, y1, z1],
        #         ...
        #     ]
        #
        # 统一转换为 float 类型的 NumPy 数组。
        self.points = np.asarray(points, dtype=float)

        # 每个节点的自由度数量。
        #
        # 例如：
        #
        # 2D 桁架：
        #     dofs_per_node = 2
        #     [ux, uy]
        #
        # 2D 梁/框架：
        #     dofs_per_node = 3
        #     [ux, uy, rz]
        #
        # 3D 桁架：
        #     dofs_per_node = 3
        #     [ux, uy, uz]
        #
        # 3D 梁/框架：
        #     dofs_per_node = 6
        #     [ux, uy, uz, rx, ry, rz]
        self.dofs_per_node = int(dofs_per_node)

        # 有限元单元集合。
        #
        # 每个单元需要至少提供：
        #
        #     element.dofs_per_node
        #
        # 后续通常还会提供：
        #
        #     element.stiffness(...)
        #     element.dof_indices(...)
        #
        self.elements = []

        # 外部集中载荷。
        #
        # key:
        #     全局自由度编号
        #
        # value:
        #     对应自由度上的载荷值
        #
        # 例如：
        #
        #     loads[3] = -1000.0
        #
        # 表示在全局自由度 3 上施加 -1000 的载荷。
        self.loads = {}

        # 位移边界条件。
        #
        # key:
        #     全局自由度编号
        #
        # value:
        #     指定的位移值
        #
        # 例如：
        #
        #     constraints[0] = 0.0
        #
        # 表示第 0 个全局自由度固定。
        self.constraints = {}

    @property
    def ndof(self):
        """返回模型总自由度数量。

        总自由度：

            ndof = 节点数量 × 每节点自由度数量
        """
        return len(self.points) * self.dofs_per_node

    def add_element(self, e):
        """向模型中添加有限元单元。

        Parameters
        ----------
        e
            有限元单元对象。

        Notes
        -----
        当前高层 StructuralModel 要求所有单元使用统一的
        nodal DOF 数量。

        例如，一个模型中不能同时直接混用：

            2D Truss: 2 DOF/node
            2D Beam:  3 DOF/node

        后续如果引入自由度管理器 DOFManager，
        可以解除这一限制。
        """

        if e.dofs_per_node != self.dofs_per_node:
            raise ValueError(
                "uniform nodal DOF count required in v1.1 " "high-level structural model"
            )

        self.elements.append(e)

    def add_load(self, dof, value):
        """在指定全局自由度上施加集中载荷。

        Parameters
        ----------
        dof : int
            全局自由度编号。

        value : float
            载荷值。

        Notes
        -----
        如果同一个自由度多次施加载荷，则载荷自动累加。
        """

        dof = int(dof)
        value = float(value)

        self.loads[dof] = self.loads.get(dof, 0.0) + value

    def constrain(self, dof, value=0.0):
        """对指定全局自由度施加位移约束。

        Parameters
        ----------
        dof : int
            全局自由度编号。

        value : float, default=0.0
            指定的位移值。

        Examples
        --------
        固定自由度：

            model.constrain(0)

        指定位移：

            model.constrain(3, 0.01)
        """

        self.constraints[int(dof)] = float(value)

    def load_vector(self):
        """组装并返回全局载荷向量。

        Returns
        -------
        numpy.ndarray
            长度为 ``ndof`` 的全局载荷向量。
        """

        f = np.zeros(self.ndof, dtype=float)

        for dof, value in self.loads.items():
            f[dof] += value

        return f
