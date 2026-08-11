#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NumPyBackend 基础使用示例。
"""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from opencaxpy.backend import NumPyBackend


def main():
    backend = NumPyBackend()

    print("=" * 72)
    print("NumPyBackend Example")
    print("=" * 72)

    print("backend name =", backend.name)

    # Python list -> ndarray
    a = backend.asarray(
        [
            [1.0, 2.0],
            [3.0, 4.0],
        ]
    )

    print("\nasarray:")
    print(a)

    # 创建全零数组
    zeros = backend.zeros((3, 2))

    print("\nzeros:")
    print(zeros)

    # 创建全一数组
    ones = backend.ones((3, 2))

    print("\nones:")
    print(ones)

    print("\ndtype =", a.dtype)
    print("shape =", a.shape)


if __name__ == "__main__":
    main()
