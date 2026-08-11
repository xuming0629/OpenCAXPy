#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BackendManager 基础使用示例。
"""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from opencaxpy.backend import backend_manager as bm


def main():
    print("=" * 72)
    print("BackendManager Example")
    print("=" * 72)

    # 当前后端
    print("current backend =", bm.name)

    # 已注册后端
    print(
        "available backends =",
        bm.available_backends,
    )

    # BackendManager 自动把方法代理给当前 Backend
    a = bm.asarray(
        [
            [1.0, 2.0],
            [3.0, 4.0],
        ]
    )

    b = bm.zeros((2, 3))
    c = bm.ones((2, 3))

    print("\nasarray:")
    print(a)

    print("\nzeros:")
    print(b)

    print("\nones:")
    print(c)

    print("\nbackend object:")
    print(type(bm.current))


if __name__ == "__main__":
    main()
