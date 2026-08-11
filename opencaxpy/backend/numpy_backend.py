#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : numpy_backend.py
# @Time          : 2026-08-11 09:48:30
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy NumPy 数组计算后端实现
# @Company       : 2026 XuMing. All Rights Reserved.
"""

import numpy as np


class NumPyBackend:
    """
    NumPy 数组计算后端。

    该类对 NumPy 常用数组操作进行统一封装，
    为 OpenCAXPy 提供一致的数组创建和转换接口。

    后续可以通过相同接口扩展其他计算后端，例如：
        - PyTorch
        - CuPy
        - JAX

    上层模块（Mesh、FEM、Solver 等）尽量通过 Backend 接口
    操作数组，减少对具体数值计算库的直接依赖。
    """

    # 当前后端名称，用于 BackendManager 注册和切换后端。
    name = "numpy"

    def asarray(self, x, dtype=None):
        """
        将输入数据转换为 NumPy 数组。

        与 np.asarray 类似：
        如果输入本身已经是满足条件的 ndarray，
        通常不会产生不必要的数据复制。

        Parameters
        ----------
        x:
            待转换的数据，可以是 list、tuple、ndarray 等。

        dtype:
            目标数据类型。
            如果为 None，则由 NumPy 自动推断。

        Returns
        -------
        numpy.ndarray
            转换后的 NumPy 数组。
        """
        return np.asarray(x, dtype=dtype)

    def zeros(self, shape, dtype=float):
        """
        创建指定形状的全零数组。

        常用于：
            - 节点坐标初始化
            - 位移向量初始化
            - 载荷向量初始化
            - 单元矩阵初始化
            - 结果数组初始化

        Parameters
        ----------
        shape:
            数组形状，例如：
                (10,)
                (10, 3)
                (6, 6)

        dtype:
            数组数据类型，默认使用 float。

        Returns
        -------
        numpy.ndarray
            指定形状的全零数组。
        """
        return np.zeros(shape, dtype=dtype)

    def ones(self, shape, dtype=float):
        """
        创建指定形状的全一数组。

        Parameters
        ----------
        shape:
            数组形状。

        dtype:
            数组数据类型，默认使用 float。

        Returns
        -------
        numpy.ndarray
            指定形状的全一数组。
        """
        return np.ones(shape, dtype=dtype)
