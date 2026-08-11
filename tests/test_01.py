#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : test_registry.py
# @description   : Registry 注册表功能学习与测试
"""

from src.opencaxpy.registry import Registry

# ============================================================
# 1. 定义一个基类和几个实现类
# ============================================================


class Solver:
    """求解器基类。"""

    def solve(self, a: float, b: float) -> float:
        raise NotImplementedError


class AddSolver(Solver):
    """加法求解器。"""

    def solve(self, a: float, b: float) -> float:
        return a + b


class SubSolver(Solver):
    """减法求解器。"""

    def solve(self, a: float, b: float) -> float:
        return a - b


class MulSolver(Solver):
    """乘法求解器。"""

    def solve(self, a: float, b: float) -> float:
        return a * b


# ============================================================
# 2. 创建注册表
# ============================================================

# 注册表保存的是 Solver 的类，而不是 Solver 实例。
solver_registry: Registry[type[Solver]] = Registry("solver")


# ============================================================
# 3. 普通方式注册
# ============================================================

solver_registry.register("add", AddSolver)
solver_registry.register("sub", SubSolver)


# ============================================================
# 4. 装饰器方式注册
# ============================================================


@solver_registry.register("divide")
class DivideSolver(Solver):
    """除法求解器。"""

    def solve(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("除数不能为 0")
        return a / b


# ============================================================
# 5. 各项功能测试
# ============================================================


def test_register_and_get() -> None:
    """测试注册和查找。"""

    print("\n========== 测试注册与查找 ==========")

    solver_class = solver_registry.get("add")

    print("查找到的对象：", solver_class)
    print("对象名称：", solver_class.__name__)

    solver = solver_class()
    result = solver.solve(10, 3)

    print("10 + 3 =", result)

    assert solver_class is AddSolver
    assert result == 13


def test_decorator_register() -> None:
    """测试装饰器注册。"""

    print("\n========== 测试装饰器注册 ==========")

    solver_class = solver_registry.get("divide")
    solver = solver_class()

    result = solver.solve(10, 2)

    print("装饰器注册的类：", solver_class)
    print("10 / 2 =", result)

    assert solver_class is DivideSolver
    assert result == 5


def test_contains() -> None:
    """测试 contains。"""

    print("\n========== 测试 contains ==========")

    print("是否存在 add：", solver_registry.contains("add"))
    print("是否存在 mul：", solver_registry.contains("mul"))

    assert solver_registry.contains("add") is True
    assert solver_registry.contains("mul") is False


def test_names() -> None:
    """测试 names，结果按名称排序。"""

    print("\n========== 测试 names ==========")

    names = solver_registry.names()

    print("所有注册名称：", names)

    assert names == ("add", "divide", "sub")


def test_items() -> None:
    """测试 items。"""

    print("\n========== 测试 items ==========")

    items = solver_registry.items()

    for name, solver_class in items:
        print(f"{name:10s} -> {solver_class.__name__}")

    assert items[0] == ("add", AddSolver)
    assert items[1] == ("divide", DivideSolver)
    assert items[2] == ("sub", SubSolver)


def test_duplicate_register() -> None:
    """测试重复注册时抛出异常。"""

    print("\n========== 测试重复注册 ==========")

    try:
        solver_registry.register("add", MulSolver)
    except KeyError as exc:
        print("捕获到预期异常：", exc)
    else:
        raise AssertionError("重复注册应该抛出 KeyError")


def test_replace_register() -> None:
    """测试 replace=True 覆盖注册。"""

    print("\n========== 测试覆盖注册 ==========")

    registry: Registry[type[Solver]] = Registry("temporary solver")

    registry.register("calculate", AddSolver)

    print("覆盖前：", registry.get("calculate").__name__)

    registry.register(
        "calculate",
        MulSolver,
        replace=True,
    )

    print("覆盖后：", registry.get("calculate").__name__)

    solver_class = registry.get("calculate")
    result = solver_class().solve(4, 5)

    print("4 * 5 =", result)

    assert solver_class is MulSolver
    assert result == 20


def test_unknown_key() -> None:
    """测试查询不存在的名称。"""

    print("\n========== 测试不存在的 key ==========")

    try:
        solver_registry.get("power")
    except KeyError as exc:
        print("捕获到预期异常：", exc)

        message = str(exc)

        assert "power" in message
        assert "available" in message
    else:
        raise AssertionError("查询不存在名称应该抛出 KeyError")


def test_empty_key() -> None:
    """测试空名称注册。"""

    print("\n========== 测试空 key ==========")

    registry: Registry[type[Solver]] = Registry("solver")

    try:
        registry.register("", AddSolver)
    except ValueError as exc:
        print("捕获到预期异常：", exc)
    else:
        raise AssertionError("空 key 应该抛出 ValueError")


def test_unregister() -> None:
    """测试删除注册项。"""

    print("\n========== 测试 unregister ==========")

    registry: Registry[type[Solver]] = Registry("temporary solver")

    registry.register("add", AddSolver)
    registry.register("sub", SubSolver)

    print("删除前：", registry.names())

    registry.unregister("add")

    print("删除后：", registry.names())

    assert registry.contains("add") is False
    assert registry.names() == ("sub",)


def test_clear() -> None:
    """测试清空注册表。"""

    print("\n========== 测试 clear ==========")

    registry: Registry[type[Solver]] = Registry("temporary solver")

    registry.register("add", AddSolver)
    registry.register("sub", SubSolver)

    print("清空前：", registry.names())

    registry.clear()

    print("清空后：", registry.names())

    assert registry.names() == ()
    assert registry.items() == ()


def test_dynamic_create_solver() -> None:
    """模拟实际业务：根据配置名称动态创建对象。"""

    print("\n========== 测试动态创建对象 ==========")

    config = {
        "solver": "sub",
        "a": 20,
        "b": 8,
    }

    solver_name = config["solver"]

    # 根据配置中的字符串查找类
    solver_class = solver_registry.get(solver_name)

    # 创建类的实例
    solver = solver_class()

    # 调用统一接口
    result = solver.solve(
        config["a"],
        config["b"],
    )

    print("配置：", config)
    print("实际类型：", type(solver).__name__)
    print("计算结果：", result)

    assert isinstance(solver, SubSolver)
    assert result == 12


# ============================================================
# 6. 普通 Python 方式运行所有测试
# ============================================================


def main() -> None:
    test_register_and_get()
    test_decorator_register()
    test_contains()
    test_names()
    test_items()
    test_duplicate_register()
    test_replace_register()
    test_unknown_key()
    test_empty_key()
    test_unregister()
    test_clear()
    test_dynamic_create_solver()

    print("\n========================================")
    print("所有 Registry 测试通过")
    print("========================================")


if __name__ == "__main__":
    main()
