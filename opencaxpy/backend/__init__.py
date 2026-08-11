#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : __init__.py
# @Time          : 2026-08-11 09:45:02
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : OpenCAXPy 数组计算后端公共接口
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from .manager import BackendManager, backend_manager
from .numpy_backend import NumPyBackend

__all__ = [
    "BackendManager",
    "backend_manager",
    "NumPyBackend",
]
