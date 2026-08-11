#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BackendManager.register_backend() 使用示例。
"""

from pathlib import Path
import sys

import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from opencaxpy.backend import BackendManager


class DemoBackend:
    """
    用于演示 Backend 注册机制的简单测试后端。
    """

    name = "demo"

    def asarray(self, x, dtype=None):
        print("[DemoBackend] asarray")
        return np.asarray(x, dtype=dtype)

    def zeros(self, shape, dtype=float):
        print("[DemoBackend] zeros")
        return np.zeros(shape, dtype=dtype)

    def ones(self, shape, dtype=float):
        print("[DemoBackend] ones")
        return np.ones(shape, dtype=dtype)


def main():
    print("=" * 72)
    print("Register Backend Example")
    print("=" * 72)

    # 使用独立 BackendManager，
    # 避免修改全局 backend_manager。
    bm = BackendManager()

    print(
        "before register =",
        bm.available_backends,
    )

    # 注册新的 Backend
    bm.register_backend(
        "demo",
        DemoBackend(),
    )

    print(
        "after register =",
        bm.available_backends,
    )

    # 切换到 Demo Backend
    bm.set_backend("demo")

    print(
        "current backend =",
        bm.name,
    )

    a = bm.zeros((2, 3))

    print("\nresult:")
    print(a)


if __name__ == "__main__":
    main()
