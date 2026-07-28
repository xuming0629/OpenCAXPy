# OpenCAXPy Git 开发流程

本文档说明 OpenCAXPy 仓库的日常开发、分支管理、Pull Request、合并、发布和紧急修复流程。

---

## 1. 当前分支状态

初始化完成后，仓库通常包含：

```text
* develop
  main
  remotes/origin/develop
  remotes/origin/main
```

其中：

```text
main
  稳定发布分支

develop
  日常开发集成分支

feature/*
  新功能开发分支

fix/*
  普通 Bug 修复分支

refactor/*
  重构分支

release/*
  发布准备分支

hotfix/*
  线上紧急修复分支
```

平时不要直接在 `main` 或 `develop` 上开发功能。

推荐流程：

```text
feature/* → develop → release/* → main
```

紧急修复流程：

```text
hotfix/* → main
         ↘ develop
```

---

## 2. 开发新功能

以开发三角形网格一致加密为例。

先切换到 `develop`：

```bash
git checkout develop
```

同步远程最新代码：

```bash
git pull --ff-only origin develop
```

创建功能分支：

```bash
git checkout -b feature/triangle-uniform-refinement
```

确认当前分支：

```bash
git branch
```

应该看到：

```text
* feature/triangle-uniform-refinement
  develop
  main
```

然后在该分支中修改代码。

---

## 3. 推荐的功能分支名称

网格功能：

```text
feature/triangle-refinement
feature/triangle-bisection
feature/quad-refinement
feature/tetra-refinement
feature/hexa-refinement
feature/hexa20
feature/hexa27
feature/mesh-quality
feature/mesh-smoothing
```

拓扑功能：

```text
feature/triangle-topology
feature/quad-topology
feature/tetra-topology
feature/hexa-topology
feature/boundary-tags
feature/nonmanifold-check
```

FEM 功能：

```text
feature/poisson2d
feature/poisson3d
feature/fem-assembly
feature/lagrange-p1
feature/lagrange-p2
feature/linear-elasticity
feature/heat-equation
```

后处理功能：

```text
feature/vtk-export
feature/vtk-cell-labels
feature/vtk-point-labels
feature/pyvista-viewer
feature/result-field
```

Bug 修复：

```text
fix/tetra-volume
fix/hexa-boundary-faces
fix/torch-device-conversion
fix/triangle-orientation
```

重构：

```text
refactor/topology-base
refactor/mesh-storage
refactor/vtk-converter
refactor/backend-manager
```

---

## 4. 开发过程中查看状态

查看修改：

```bash
git status
```

查看具体差异：

```bash
git diff
```

查看已经加入暂存区的修改：

```bash
git diff --cached
```

查看最近提交：

```bash
git log --oneline --graph --decorate -10
```

---

## 5. 运行自动测试

运行全部测试：

```bash
pytest -q
```

运行指定测试文件：

```bash
pytest tests/test_triangle.py -v
```

运行指定测试函数：

```bash
pytest tests/test_triangle.py::test_triangle_mesh_counts_and_area -v
```

运行 PyTorch 后端测试：

```bash
pytest tests/test_torch_backend.py -v
```

运行覆盖率：

```bash
pytest \
  --cov=opencaxpy \
  --cov-report=term-missing \
  --cov-report=html
```

HTML 覆盖率报告生成在：

```text
htmlcov/index.html
```

---

## 6. 运行代码质量检查

检查代码：

```bash
ruff check .
```

检查格式：

```bash
ruff format --check .
```

自动修复 Ruff 能处理的问题：

```bash
ruff check . --fix
```

自动格式化：

```bash
ruff format .
```

运行完整本地检查：

```bash
./scripts/check.sh
```

该脚本通常执行：

```bash
ruff check .
ruff format --check .
pytest --cov=opencaxpy --cov-report=term-missing
python -m build
python -m twine check dist/*
```

---

## 7. 提交代码

添加全部修改：

```bash
git add .
```

或者只添加指定文件：

```bash
git add src/opencaxpy/mesh/refinement.py
git add tests/test_triangle_refinement.py
```

提交：

```bash
git commit -m "feat(mesh): add triangle uniform refinement"
```

开发过程中可以有多个提交：

```bash
git commit -m "feat(mesh): add triangle uniform refinement"
git commit -m "test(mesh): add triangle refinement tests"
git commit -m "docs(mesh): document refinement API"
```

---

## 8. Commit 提交规范

采用 Conventional Commits：

```text
类型(模块): 描述
```

常用类型：

```text
feat
  新功能

fix
  Bug 修复

test
  测试

refactor
  重构

docs
  文档

perf
  性能优化

ci
  CI/CD

build
  构建系统

chore
  工程维护
```

示例：

```bash
git commit -m "feat(mesh): add Triangle6 conversion"
git commit -m "fix(topology): correct Hexa8 face orientation"
git commit -m "test(mesh): add Quad9 topology tests"
git commit -m "refactor(post): split VTK viewer and exporter"
git commit -m "docs(readme): add development workflow"
git commit -m "perf(topology): optimize edge construction"
git commit -m "ci(actions): add Python 3.13 tests"
git commit -m "build(package): update optional dependencies"
git commit -m "chore(release): prepare version 0.3.0"
```

不建议：

```text
update
fix bug
修改代码
提交一下
```

---

## 9. 推送功能分支

第一次推送：

```bash
git push -u origin feature/triangle-uniform-refinement
```

后续继续提交后，只需要：

```bash
git push
```

查看远程分支：

```bash
git branch -r
```

查看全部本地和远程分支：

```bash
git branch -a
```

---

## 10. 创建 Pull Request

在 GitHub 仓库页面创建 Pull Request。

目标分支：

```text
base: develop
```

源分支：

```text
compare: feature/triangle-uniform-refinement
```

对应关系：

```text
feature/triangle-uniform-refinement
                 ↓
              develop
```

PR 标题建议：

```text
feat(mesh): add triangle uniform refinement
```

PR 内容建议包括：

```text
实现内容
接口变化
测试结果
网格节点与单元数量变化
面积或体积检查结果
NumPy 后端测试结果
PyTorch 后端测试结果
相关 Issue
```

---

## 11. CI 自动检查

创建 PR 后，GitHub Actions 会自动执行：

```text
Ruff 代码检查
Ruff 格式检查
Python 3.10 测试
Python 3.11 测试
Python 3.12 测试
Python 3.13 测试
PyTorch CPU 后端测试
pytest 覆盖率
Wheel 构建
源码包构建
Twine 包检查
CodeQL 安全分析
PR 标题规范检查
```

只有全部检查通过后再合并。

---

## 12. 合并 Pull Request

推荐使用：

```text
Squash and merge
```

这样一个 PR 在 `develop` 中只保留一个清晰提交。

Squash 提交标题继续使用：

```text
feat(mesh): add triangle uniform refinement
```

不建议对普通功能 PR 使用：

```text
Merge commit
```

除非需要保留完整的分支提交历史。

---

## 13. PR 合并后的本地同步

PR 合并到 `develop` 后：

```bash
git checkout develop
git pull --ff-only origin develop
```

删除本地功能分支：

```bash
git branch -d feature/triangle-uniform-refinement
```

删除远程功能分支：

```bash
git push origin --delete feature/triangle-uniform-refinement
```

如果 GitHub 已自动删除远程分支，就不需要再次执行删除命令。

---

## 14. 日常开发完整流程

每次开发新功能，可以直接采用以下流程：

```bash
git checkout develop
git pull --ff-only origin develop

git checkout -b feature/功能名称

# 修改代码

pytest -q
ruff check .
ruff format --check .

git add .
git commit -m "feat(模块): 功能描述"

git push -u origin feature/功能名称
```

然后在 GitHub 创建：

```text
feature/功能名称 → develop
```

的 Pull Request。

PR 合并后：

```bash
git checkout develop
git pull --ff-only origin develop

git branch -d feature/功能名称
git push origin --delete feature/功能名称
```

---

## 15. 普通 Bug 修复

普通 Bug 从 `develop` 创建：

```bash
git checkout develop
git pull --ff-only origin develop

git checkout -b fix/hexa-boundary-faces
```

修复后：

```bash
pytest -q
ruff check .
ruff format --check .

git add .
git commit -m "fix(topology): correct Hexa8 boundary faces"
git push -u origin fix/hexa-boundary-faces
```

创建 PR：

```text
fix/hexa-boundary-faces → develop
```

---

## 16. 处理 develop 更新

如果你开发期间 `develop` 有新提交，可以把最新内容合并到功能分支。

推荐使用 rebase：

```bash
git checkout develop
git pull --ff-only origin develop

git checkout feature/triangle-uniform-refinement
git rebase develop
```

如果发生冲突：

```bash
git status
```

手动修改冲突文件，然后：

```bash
git add 冲突文件
git rebase --continue
```

取消 rebase：

```bash
git rebase --abort
```

如果该功能分支已经推送过远程，rebase 后需要：

```bash
git push --force-with-lease
```

不要使用：

```bash
git push --force
```

推荐使用更安全的：

```bash
git push --force-with-lease
```

---

## 17. 暂存未完成修改

临时切换分支前，可以暂存当前修改：

```bash
git stash push -m "triangle refinement work"
```

查看 stash：

```bash
git stash list
```

恢复：

```bash
git stash pop
```

只恢复但不删除 stash：

```bash
git stash apply stash@{0}
```

---

## 18. main 分支使用原则

`main` 只存放稳定版本。

普通开发：

```text
feature/* → develop
```

发布：

```text
develop → release/x.y.z → main
```

不要直接在 `main` 上开发功能。

不要日常直接执行：

```bash
git push origin main
```

除非是：

```text
发布版本
合并 hotfix
推送版本标签
```

---

## 19. 发布新版本

当 `develop` 中功能稳定后，创建发布分支。

```bash
git checkout develop
git pull --ff-only origin develop

git checkout -b release/0.3.0
```

修改版本信息：

```text
pyproject.toml
src/opencaxpy/__init__.py
CHANGELOG.md
```

例如：

```toml
version = "0.3.0"
```

Python 包版本：

```python
__version__ = "0.3.0"
```

更新日志：

```markdown
## [0.3.0]

### Added

- Triangle uniform refinement.
- Mesh quality evaluation.
- VTK node and cell labels.
```

提交发布准备：

```bash
git add .
git commit -m "chore(release): prepare version 0.3.0"
git push -u origin release/0.3.0
```

创建 PR：

```text
release/0.3.0 → main
```

---

## 20. 发布标签

发布 PR 合并到 `main` 后：

```bash
git checkout main
git pull --ff-only origin main
```

创建标签：

```bash
git tag -a v0.3.0 -m "OpenCAXPy v0.3.0"
```

推送标签：

```bash
git push origin v0.3.0
```

标签会触发自动发布：

```text
运行测试
构建 Wheel
构建源码包
检查发布包
创建 GitHub Release
上传构建产物
发布到 PyPI
```

查看标签：

```bash
git tag
```

查看标签信息：

```bash
git show v0.3.0
```

---

## 21. 发布后同步 develop

版本发布后，把 `main` 同步回 `develop`：

```bash
git checkout develop
git pull --ff-only origin develop

git merge --no-ff main
git push origin develop
```

然后可以删除发布分支：

```bash
git branch -d release/0.3.0
git push origin --delete release/0.3.0
```

---

## 22. 紧急修复 Hotfix

线上稳定版本出现紧急 Bug 时，从 `main` 创建：

```bash
git checkout main
git pull --ff-only origin main

git checkout -b hotfix/0.3.1
```

修复并测试：

```bash
pytest -q
ruff check .
ruff format --check .
```

提交：

```bash
git add .
git commit -m "fix(topology): correct Hexa8 boundary face detection"
git push -u origin hotfix/0.3.1
```

创建 PR：

```text
hotfix/0.3.1 → main
```

合并后：

```bash
git checkout main
git pull --ff-only origin main

git tag -a v0.3.1 -m "OpenCAXPy v0.3.1"
git push origin v0.3.1
```

再同步到 `develop`：

```bash
git checkout develop
git pull --ff-only origin develop
git merge --no-ff main
git push origin develop
```

删除 hotfix 分支：

```bash
git branch -d hotfix/0.3.1
git push origin --delete hotfix/0.3.1
```

---

## 23. 撤销未提交修改

撤销某个文件的未提交修改：

```bash
git restore 文件路径
```

例如：

```bash
git restore src/opencaxpy/mesh/mesh.py
```

撤销所有未提交修改：

```bash
git restore .
```

取消暂存：

```bash
git restore --staged 文件路径
```

取消全部暂存：

```bash
git restore --staged .
```

---

## 24. 修改最近一次提交

修改最近一次提交信息：

```bash
git commit --amend -m "feat(mesh): add triangle refinement"
```

把漏掉的文件补进最近提交：

```bash
git add 漏掉的文件
git commit --amend --no-edit
```

如果该提交已推送远程：

```bash
git push --force-with-lease
```

---

## 25. 撤销已经提交的修改

推荐使用 `git revert`，保留历史：

```bash
git revert 提交哈希
```

例如：

```bash
git revert a1b2c3d
```

然后：

```bash
git push
```

不要轻易在共享分支使用：

```bash
git reset --hard
```

---

## 26. 删除错误分支

删除本地分支：

```bash
git branch -d 分支名
```

强制删除未合并本地分支：

```bash
git branch -D 分支名
```

删除远程分支：

```bash
git push origin --delete 分支名
```

---

## 27. 查看远程信息

查看远程地址：

```bash
git remote -v
```

查看远程详细信息：

```bash
git remote show origin
```

同步远程分支信息：

```bash
git fetch origin
```

删除本地已经不存在的远程分支引用：

```bash
git fetch --prune
```

---

## 28. 推荐的本地开发环境

创建虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

升级 pip：

```bash
python -m pip install --upgrade pip
```

安装开发依赖：

```bash
python -m pip install -e ".[dev]"
```

安装 PyTorch 后端：

```bash
python -m pip install -e ".[torch]"
```

安装 VTK 后处理：

```bash
python -m pip install -e ".[visual]"
```

全部安装：

```bash
python -m pip install -e ".[dev,torch,visual]"
```

安装 pre-commit：

```bash
pre-commit install
```

手动运行全部 pre-commit 检查：

```bash
pre-commit run --all-files
```

---

## 29. 推荐的 GitHub 仓库设置

在 GitHub 中进入：

```text
Repository
→ Settings
→ Rules
→ Rulesets
```

为 `main` 和 `develop` 设置保护规则。

建议开启：

```text
Require a pull request before merging
Require approvals
Dismiss stale approvals
Require review from Code Owners
Require status checks to pass
Require branches to be up to date
Require conversation resolution
Block force pushes
Restrict deletions
Require linear history
```

建议仅保留：

```text
Squash merging
```

建议自动删除已合并分支：

```text
Settings
→ General
→ Pull Requests
→ Automatically delete head branches
```

---

## 30. 开发三角形加密示例

开始开发：

```bash
git checkout develop
git pull --ff-only origin develop

git checkout -b feature/triangle-uniform-refinement
```

开发完成后测试：

```bash
pytest -q
ruff check .
ruff format --check .
```

提交：

```bash
git add .
git commit -m "feat(mesh): add triangle uniform refinement"
```

推送：

```bash
git push -u origin feature/triangle-uniform-refinement
```

创建 PR：

```text
feature/triangle-uniform-refinement → develop
```

合并后：

```bash
git checkout develop
git pull --ff-only origin develop

git branch -d feature/triangle-uniform-refinement
git push origin --delete feature/triangle-uniform-refinement
```

---

## 31. 开发 FEM 示例

创建分支：

```bash
git checkout develop
git pull --ff-only origin develop

git checkout -b feature/poisson2d
```

提交建议：

```bash
git commit -m "feat(fem): add Triangle3 shape functions"
git commit -m "feat(fem): add Poisson2D assembler"
git commit -m "test(fem): add Poisson2D convergence test"
git commit -m "docs(fem): add Poisson2D example"
```

推送：

```bash
git push -u origin feature/poisson2d
```

创建：

```text
feature/poisson2d → develop
```

的 Pull Request。

---

## 32. 常用命令速查

更新开发分支：

```bash
git checkout develop
git pull --ff-only origin develop
```

创建功能分支：

```bash
git checkout -b feature/name
```

查看状态：

```bash
git status
```

提交：

```bash
git add .
git commit -m "feat(module): description"
```

推送：

```bash
git push -u origin feature/name
```

合并后清理：

```bash
git checkout develop
git pull --ff-only origin develop
git branch -d feature/name
git push origin --delete feature/name
```

查看提交：

```bash
git log --oneline --graph --decorate --all
```

查看分支：

```bash
git branch -a
```

查看标签：

```bash
git tag
```

同步远程：

```bash
git fetch --prune
```
