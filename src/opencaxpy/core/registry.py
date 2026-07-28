#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : registry.py
# @Time          : 2026-07-28 10:21:55
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : TODO
# @Company       : 2026 XuMing. All Rights Reserved.
"""



from __future__ import annotations

from collections.abc import Callable
from typing import Generic, TypeVar


T = TypeVar("T")


class Registry(Generic[T]):
    """Small explicit registry used by extensible CAX components."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._items: dict[str, T] = {}

    def register(
        self,
        key: str,
        value: T | None = None,
        *,
        replace: bool = False,
    ):
        if value is None:
            def decorator(item: T) -> T:
                self.register(key, item, replace=replace)
                return item
            return decorator

        if not key:
            raise ValueError("registry key cannot be empty")

        if key in self._items and not replace:
            raise KeyError(
                f"{key!r} is already registered in {self.name}"
            )

        self._items[key] = value
        return value

    def unregister(self, key: str) -> None:
        del self._items[key]

    def get(self, key: str) -> T:
        try:
            return self._items[key]
        except KeyError as exc:
            raise KeyError(
                f"unknown {self.name} entry {key!r}; "
                f"available={sorted(self._items)}"
            ) from exc

    def contains(self, key: str) -> bool:
        return key in self._items

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._items))

    def items(self) -> tuple[tuple[str, T], ...]:
        return tuple((key, self._items[key]) for key in sorted(self._items))

    def clear(self) -> None:
        self._items.clear()
