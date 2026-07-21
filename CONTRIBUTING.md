# OpenCAXPy 贡献指南

## 分支模型

OpenCAXPy 使用精简 Git Flow。

```text
main
  └── 稳定版本，仅接收 release/* 和 hotfix/*

develop
  └── 日常集成分支

feature/*
  └── 从 develop 创建，新功能完成后合并回 develop

fix/*
  └── 从 develop 创建，普通缺陷修复后合并回 develop

release/*
  └── 从 develop 创建，只允许版本号、文档和发布修复

hotfix/*
  └── 从 main 创建，紧急修复后同时合并到 main 和 develop
```

## 初始化分支

仓库第一次创建后执行：

```bash
git branch -M main
git push -u origin main

git checkout -b develop
git push -u origin develop
```

以后将 GitHub 默认分支设置为 `develop`，日常开发 PR 默认合并到
`develop`。稳定发布仍从 `main` 打标签。

## 新功能开发

```bash
git checkout develop
git pull --ff-only origin develop

git checkout -b feature/triangle-refine
```

提交：

```bash
git add .
git commit -m "feat(mesh): add triangle uniform refinement"
git push -u origin feature/triangle-refine
```

然后创建：

```text
feature/triangle-refine -> develop
```

的 Pull Request。

## 发布流程

准备发布：

```bash
git checkout develop
git pull --ff-only origin develop
git checkout -b release/0.3.0
```

在 `release/0.3.0` 中：

1. 修改 `pyproject.toml` 版本号。
2. 修改 `src/opencaxpy/__init__.py` 的 `__version__`。
3. 更新 `CHANGELOG.md`。
4. 运行全部测试。
5. 创建 `release/0.3.0 -> main` 的 PR。

合并后：

```bash
git checkout main
git pull --ff-only origin main

git tag -a v0.3.0 -m "OpenCAXPy v0.3.0"
git push origin v0.3.0
```

标签会触发 Release 工作流：

```text
测试
→ 构建 wheel 和 source distribution
→ 创建 GitHub Release
→ 通过 PyPI Trusted Publishing 发布
```

最后将 `main` 同步回 `develop`：

```bash
git checkout develop
git merge --no-ff main
git push origin develop
```

## 紧急修复

```bash
git checkout main
git pull --ff-only origin main
git checkout -b hotfix/0.3.1
```

修复后先 PR 到 `main`，打 `v0.3.1` 标签，然后把 `main` 合并回
`develop`。

## Commit 和 PR 标题规范

采用 Conventional Commits：

```text
feat(mesh): add Triangle6 element
fix(topology): correct Hexa8 boundary faces
refactor(post): split VTK converter and viewer
test(mesh): add tetrahedron volume tests
docs(readme): document PyTorch backend
ci(actions): add Python 3.13 test
```

允许的类型：

```text
feat fix docs test refactor perf build ci chore
```

## 本地开发

```bash
python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

pre-commit install
pytest
ruff check .
ruff format --check .
```

自动修复格式：

```bash
ruff check . --fix
ruff format .
```

## Pull Request 合并要求

PR 至少满足：

1. CI 全部通过。
2. 至少一名维护者批准。
3. 分支已更新到目标分支最新状态。
4. 禁止直接推送到 `main` 和 `develop`。
5. 使用 Squash merge。
6. PR 标题符合 Conventional Commits。
7. 新功能必须有测试。
