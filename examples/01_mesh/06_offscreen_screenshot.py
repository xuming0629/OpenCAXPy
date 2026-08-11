#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @FileName      : hexahedron_vtk_offscreen.py
# @Time          : 2026-08-11
# @Author        : XuMing
# @Email         : 920972751@qq.com
# @description   : Hexa8 网格 VTK 离屏渲染并保存截图示例
# @Company       : 2026 XuMing. All Rights Reserved.
"""

from pathlib import Path
import sys

# ============================================================
# 项目根目录
# ============================================================

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


from opencaxpy import (
    HexahedronMesh,
    VTKMeshViewer,
    VTKMeshViewerOptions,
)


def main():
    # ========================================================
    # 1. 创建 Hexa8 网格
    # ========================================================
    #
    # 区域：
    #   x in [0, 2]
    #   y in [0, 1]
    #   z in [0, 1]
    #
    # 划分：
    #   nx = 2
    #   ny = 1
    #   nz = 1
    #
    # 因此会生成 2 个 Hexa8 单元。
    #
    mesh = HexahedronMesh.from_box(
        box=(0.0, 2.0, 0.0, 1.0, 0.0, 1.0),
        nx=2,
        ny=1,
        nz=1,
    )

    # ========================================================
    # 2. 创建 VTK Viewer
    # ========================================================
    #
    # 这里不一定要弹出交互窗口，
    # 可以直接用 save_screenshot() 做离屏截图。
    #
    viewer = VTKMeshViewer(
        mesh,
        VTKMeshViewerOptions(
            show_surface=True,  # 显示单元表面
            show_edges=True,  # 显示网格边
            show_nodes=True,  # 显示节点
            show_cell_ids=True,  # 显示单元编号
            title="Hexa8 Offscreen",
        ),
    )

    # ========================================================
    # 3. 保存截图
    # ========================================================
    #
    # scale=2 表示以更高分辨率导出，
    # 通常比默认更清晰。
    #
    output_path = ROOT / "hexa_vtk.png"

    viewer.save_screenshot(
        output_path,
        scale=2,
    )

    # ========================================================
    # 4. 关闭 Viewer
    # ========================================================
    #
    # 离屏渲染结束后建议显式关闭，释放资源。
    #
    viewer.close()

    print("saved:", output_path)


if __name__ == "__main__":
    main()
