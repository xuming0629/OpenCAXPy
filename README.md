# OpenCAXPy v0.2.0

本版将拓扑按单元族独立拆分，并新增 VTK 后处理。

## 独立拓扑

```text
mesh/topology/
├── base.py
├── factory.py
├── triangle.py
├── quadrilateral.py
├── tetrahedron.py
├── hexahedron.py
└── utils.py
```

统一接口仍然是 `mesh.topology`，实际返回 `TriangleTopology`、`QuadrilateralTopology`、`TetrahedronTopology` 或 `HexahedronTopology`。

## VTK 后处理

无需安装 VTK 即可导出 VTU：

```python
mesh.write_vtu('mesh.vtu')
```

安装可视化依赖：

```bash
pip install -e '.[visual]'
```

交互显示：

```python
mesh.show(scalars='temperature', show_edges=True, show_node_ids=True)
```

## GitHub 开发与 CI/CD

仓库采用：

```text
main       稳定发布
develop    日常集成
feature/*  新功能
fix/*      普通修复
release/*  发布准备
hotfix/*   线上紧急修复
```

初始化：

```bash
chmod +x scripts/bootstrap_git.sh
./scripts/bootstrap_git.sh
```

本地质量检查：

```bash
python -m pip install -e ".[dev]"
pre-commit install
./scripts/check.sh
```

详细说明：

- `CONTRIBUTING.md`
- `docs/BRANCH_PROTECTION.md`
- `docs/RELEASE.md`
