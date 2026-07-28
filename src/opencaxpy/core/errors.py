#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : errors.py
# @Time          : 2026-07-28 10:21:40
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : 
# @Company       : 2026 XuMing. All Rights Reserved.
"""



class OpenCAXError(Exception):
    """Base exception for OpenCAXPy."""


class BackendError(OpenCAXError):
    """Raised for backend configuration or conversion errors."""


class CellTypeError(OpenCAXError):
    """Raised for invalid or unsupported cell descriptors."""


class TopologyError(OpenCAXError):
    """Raised while building or querying topology."""
