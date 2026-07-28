# OpenCAXPy v1.0 Architecture

## Dependency direction

```text
core
  ↑
mesh
```

v1.0 只有两层。

未来扩展方向：

```text
core
  ↑
geometry     mesh
   ↑          ↑
   └── meshing
              ↑
       functionspace
              ↑
             fem
              ↑
            solver

mesh + results
      ↓
     post
```

## Backend boundary

只有数组创建、转换和基础运算经过 `ArrayBackend`。

拓扑构建在 v1.0 中使用后端无关的 Python 控制逻辑，最终结果回写到当前后端。这使 NumPy 和 PyTorch 使用相同拓扑规则，避免复制两套实现。

后续可以增加：

```text
CuPyBackend
JaxBackend
PaddleBackend
```

而不修改 Mesh API。

## High-order topology

基础拓扑只使用 `CellDescriptor.corner_nodes`。

高阶边节点由：

```python
CellDescriptor.local_edges
Topology.high_order_edge_nodes()
```

单独管理。

因此：

```text
Triangle3 / Triangle6 共享基础拓扑
Quad4 / Quad8 / Quad9 共享基础拓扑
```
