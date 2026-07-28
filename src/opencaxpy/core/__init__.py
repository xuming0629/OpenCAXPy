#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : __init__.py
# @Time          : 2026-07-28 10:21:06
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : TODO
# @Company       : 2026 XuMing. All Rights Reserved.
"""


from .backend import (
    ArrayBackend,
    BackendManager,
    NumPyBackend,
    TorchBackend,
    backend_manager,
    get_backend,
    set_default_backend,
)
from .errors import (
    BackendError,
    CellTypeError,
    OpenCAXError,
    TopologyError,
)
from .registry import Registry

__all__ = [
    "ArrayBackend",
    "NumPyBackend",
    "TorchBackend",
    "BackendManager",
    "backend_manager",
    "get_backend",
    "set_default_backend",
    "Registry",
    "OpenCAXError",
    "BackendError",
    "CellTypeError",
    "TopologyError",
]
