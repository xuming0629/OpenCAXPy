#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Backend 切换机制示例。
"""

from pathlib import Path
import sys

import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from opencaxpy.backend import BackendManager


class DemoBackend:
    name = "demo"

    def asarray(self, x, dtype=None):
        return np.asarray(
            x,
            dtype=dtype,
        )

    def zeros(self, shape, dtype=float):
        return np.zeros(
            shape,
            dtype=dtype,
        )

    def ones(self, shape, dtype=float):
        return np.ones(
            shape,
            dtype=dtype,
        )


def main():
    print("=" * 72)
    print("Backend Switch Example")
    print("=" * 72)

    bm = BackendManager()

    bm.register_backend(
        "demo",
        DemoBackend(),
    )

    print(
        "available backends =",
        bm.available_backends,
    )

    # ------------------------------------------------------------
    # NumPy Backend
    # ------------------------------------------------------------

    bm.set_backend("numpy")

    print("\ncurrent backend =", bm.name)

    a = bm.ones((2, 2))

    print(a)

    # ------------------------------------------------------------
    # Demo Backend
    # ------------------------------------------------------------

    bm.set_backend("demo")

    print("\ncurrent backend =", bm.name)

    b = bm.ones((2, 2))

    print(b)


if __name__ == "__main__":
    main()
