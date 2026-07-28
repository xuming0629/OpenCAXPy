# OpenCAXPy Mesh Kernel v0.5

OpenCAXPy Mesh Kernel 是一个面向 CAE、有限元、网格生成、CAD 关联和 GUI 的 Python 原生网格拓扑内核。

## v0.5 已实现

- 统一 `Mesh` 数据模型
- `Geometry` 坐标存储
- `ElementDescriptor` 元素局部拓扑
- `Connectivity` CSR 邻接存储
- `Topology` 通用维度连接查询
- `TopologyBuilder`
- Triangle3
- Quad4
- Tetra4
- Hexa8
- `cell -> vertex`
- `cell -> edge`
- `edge -> vertex`
- `edge -> cell`
- `cell -> face`
- `face -> vertex`
- `face -> edge`
- `face -> cell`
- `edge -> face`
- `cell -> cell`
- 边界边、边界面、边界顶点提取
- 非流形实体检测
- 节点、边、面、单元数据字段
- 高阶节点类型定义和元素注册表框架
- pytest 完整测试

## 安装

```bash
pip install -e ".[test]"
```

## 测试

```bash
pytest
```

## 示例

```python
import numpy as np
from opencaxpy import Mesh, CellType

points = np.array([
    [0.0, 0.0],
    [1.0, 0.0],
    [0.0, 1.0],
    [1.0, 1.0],
])

cells = np.array([
    [0, 1, 2],
    [1, 3, 2],
])

mesh = Mesh(points, cells, CellType.TRIANGLE3)
mesh.build_topology()

print(mesh.topology.connectivity(2, 1))  # cell -> edge
print(mesh.topology.connectivity(1, 2))  # edge -> cell
print(mesh.boundary_edges())
print(mesh.cell_neighbors(0))
```

## Extensible meshing v0.9

The meshing module now provides:

- generator registry and plugin interface
- structured Triangle/Quad/Tetra/Hexa generators
- arbitrary polygon Triangle3 generation
- disk and L-shaped special meshes
- uniform Triangle3 and Quad4 refinement
- Triangle6, Quad8/Quad9 and Tetra10 conversion
- triangle quality metric
- FEALPy-style 2D Matplotlib plot backend
- VTK Viewer retained for interactive 3D/post-processing

Examples are under `examples/meshing/`.


## v1.0 Fifth-stage Meshing

See `docs/FIFTH_STAGE_MESHING.md`.
