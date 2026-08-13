#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : problem.py
# @Time          : 2026-08-11 22:48:36
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy 问题定义及物理对象组织
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from dataclasses import dataclass, field


@dataclass
class Problem:
    """
    OpenCAXPy 通用问题定义类。

    Problem 用于描述一个完整的 CAX / 数值仿真问题，
    负责组织求解过程中需要的高层对象，例如：

        - 几何 / 网格模型；
        - 物理模型；
        - 未知场 / 状态场；
        - 边界条件；
        - 外部载荷；
        - 初始条件。

    Problem 本身主要承担“问题定义”和“数据组织”的职责，
    不直接负责：

        - 数值离散；
        - 自由度编号；
        - 矩阵装配；
        - 线性 / 非线性求解；
        - 时间积分；
        - 后处理。

    这些功能应分别由：

        Discretization
        FunctionSpace
        Assembly
        Solver
        Analysis
        Result

    等模块负责。

    Parameters
    ----------
    model : object
        当前问题对应的计算模型。

        model 可以根据 OpenCAXPy 后续架构具体定义为：

            Geometry
            Mesh
            Model

        或包含几何、材料区域、网格等信息的更高层模型对象。

    physics : list
        当前问题包含的物理模型列表。

        例如：

            LinearElasticity
            HeatTransfer
            Poisson
            NavierStokes

        多物理场问题中可以同时包含多个 physics。

    fields : dict
        当前问题中的 Field 集合。

        使用字段名称作为 key：

            {
                "displacement": displacement_field,
                "temperature": temperature_field,
            }

    boundary_conditions : list
        边界条件列表。

        例如：

            DirichletBC
            NeumannBC
            RobinBC

    loads : list
        外部载荷列表。

        例如：

            PointLoad
            SurfaceLoad
            BodyForce
            PressureLoad

    initial_conditions : list
        初始条件列表。

        主要用于：

            - 瞬态分析；
            - 动力学；
            - 热传导；
            - CFD；
            - 多物理场时间积分。
    """

    # =================================================================
    # 计算模型
    # =================================================================

    model: object

    # =================================================================
    # 物理模型
    # =================================================================

    # 使用 default_factory 避免多个 Problem 实例共享同一个 list。
    physics: list = field(default_factory=list)

    # =================================================================
    # Field
    # =================================================================

    # Field 使用名称进行索引。
    #
    # 例如：
    #
    #     problem.fields["displacement"]
    #     problem.fields["temperature"]
    #
    fields: dict = field(default_factory=dict)

    # =================================================================
    # Boundary Conditions
    # =================================================================

    boundary_conditions: list = field(default_factory=list)

    # =================================================================
    # Loads
    # =================================================================

    loads: list = field(default_factory=list)

    # =================================================================
    # Initial Conditions
    # =================================================================

    initial_conditions: list = field(default_factory=list)

    # =================================================================
    # Field Management
    # =================================================================

    def add_field(self, field):
        """
        向 Problem 注册一个 Field。

        Field 使用：

            field.name

        作为唯一名称保存到：

            self.fields

        Parameters
        ----------
        field : object
            待添加的 Field 对象。

            Field 至少需要提供：

                field.name

            属性。

        Returns
        -------
        object
            返回传入的 Field 对象。

        Examples
        --------
        假设：

            displacement = Field(
                name="displacement",
                ...
            )

        则：

            problem.add_field(displacement)

        后续可以通过：

            problem.fields["displacement"]

        获取该 Field。

        Notes
        -----
        当前实现中，如果添加一个同名 Field：

            field.name

        已经存在，则新的 Field 会覆盖原 Field。

        如果后续希望严格限制重复名称，
        可以增加 duplicate check。
        """

        # -------------------------------------------------------------
        # 使用 Field.name 作为字典 key
        # -------------------------------------------------------------

        self.fields[field.name] = field

        # 返回 Field 本身，
        # 方便链式或直接变量赋值使用。
        return field
