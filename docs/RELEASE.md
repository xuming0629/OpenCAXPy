# 自动发布配置

## GitHub Release

推送符合 `v*.*.*` 的标签会自动创建 GitHub Release：

```bash
git tag -a v0.3.0 -m "OpenCAXPy v0.3.0"
git push origin v0.3.0
```

## PyPI Trusted Publishing

第一次发布前，需要在 PyPI 创建项目或添加 Pending Publisher。

配置值：

```text
PyPI project: opencaxpy
Owner: 你的 GitHub 用户名或组织
Repository: OpenCAXPy
Workflow: release.yml
Environment: pypi
```

GitHub 仓库中还需要创建 Environment：

```text
Settings
→ Environments
→ New environment
→ pypi
```

建议为 `pypi` 环境增加人工审批，避免误标签直接发布。

Trusted Publishing 不需要在 GitHub 中保存 PyPI API Token。
