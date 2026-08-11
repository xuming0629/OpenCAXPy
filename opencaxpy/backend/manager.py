#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : manager.py
# @Time          : 2026-08-11 09:46:07
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy 数组计算后端管理器
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from .numpy_backend import NumPyBackend


class BackendManager:
    """
    OpenCAXPy 数组计算后端管理器。

    BackendManager 负责统一管理不同的数组计算后端，例如：

        - NumPy
        - PyTorch
        - CuPy
        - JAX

    上层模块可以通过 backend_manager 访问当前激活的后端，
    而不需要直接依赖某一个具体数值库。

    例如：

        from opencaxpy.backend import backend_manager as bm

        a = bm.zeros((10, 3))
        b = bm.asarray([1.0, 2.0, 3.0])

    当前默认后端为 NumPy。
    """

    def __init__(self):
        """
        初始化后端管理器。

        默认注册 NumPyBackend，并将 NumPy 设置为当前计算后端。
        """

        # 保存所有已经注册的计算后端。
        #
        # key:
        #     后端名称，例如 "numpy"、"torch"、"cupy"
        #
        # value:
        #     对应的 Backend 实例。
        self._backends = {
            "numpy": NumPyBackend(),
        }

        # 当前正在使用的后端名称。
        self._name = "numpy"

    def register_backend(self, name, backend):
        """
        注册新的数组计算后端。

        Parameters
        ----------
        name : str
            后端名称，例如：
                "numpy"
                "torch"
                "cupy"

        backend : object
            后端实例，例如：
                NumPyBackend()
                TorchBackend()
                CuPyBackend()

        Raises
        ------
        KeyError
            当指定名称已经被注册时抛出。

        Examples
        --------
        >>> backend_manager.register_backend(
        ...     "torch",
        ...     TorchBackend(),
        ... )
        """

        if name in self._backends:
            raise KeyError(f"Backend {name!r} is already registered.")

        self._backends[name] = backend

    def set_backend(self, name):
        """
        切换当前数组计算后端。

        Parameters
        ----------
        name : str
            后端名称，例如：
                "numpy"
                "torch"
                "cupy"

        Raises
        ------
        KeyError
            当指定的后端尚未注册时抛出。

        Examples
        --------
        >>> backend_manager.set_backend("numpy")
        """

        if name not in self._backends:
            raise KeyError(
                f"Backend {name!r} is not registered. "
                f"Available backends: "
                f"{list(self._backends.keys())}"
            )

        self._name = name

    @property
    def current(self):
        """
        获取当前激活的 Backend 实例。

        Returns
        -------
        object
            当前后端对象，例如 NumPyBackend。
        """

        return self._backends[self._name]

    @property
    def name(self):
        """
        获取当前后端名称。

        Returns
        -------
        str
            当前后端名称，例如 "numpy"。
        """

        return self._name

    @property
    def available_backends(self):
        """
        获取所有已经注册的后端名称。

        Returns
        -------
        tuple[str, ...]
            已注册后端名称。
        """

        return tuple(self._backends.keys())

    def __getattr__(self, name):
        """
        将未在 BackendManager 中定义的属性访问，
        自动转发到当前 Backend。

        例如：

            backend_manager.zeros((10, 3))

        实际等价于：

            backend_manager.current.zeros((10, 3))

        Parameters
        ----------
        name : str
            要访问的属性或方法名称。

        Returns
        -------
        Any
            当前 Backend 中对应的属性或方法。
        """

        return getattr(self.current, name)


# 全局 BackendManager 实例。
#
# OpenCAXPy 内部建议统一使用该实例访问数组计算能力：
#
#     from opencaxpy.backend import backend_manager as bm
#
#     points = bm.asarray(points)
#     values = bm.zeros((100,))
#
backend_manager = BackendManager()
