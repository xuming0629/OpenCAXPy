#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : __init__.py
# @Time          : 2026-08-11 10:43:04
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : 外部网格对象与 OpenCAXPy Mesh 之间的适配器。
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from .gmsh import from_gmsh
from .meshio import from_meshio

__all__ = [
    "from_gmsh",
    "from_meshio",
]
