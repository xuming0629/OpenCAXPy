# GitHub 分支保护配置

仓库文件无法自动开启 GitHub 规则，请在 GitHub 网页中配置 Rulesets。

## main 规则

路径：

```text
Repository
→ Settings
→ Rules
→ Rulesets
→ New branch ruleset
```

目标分支：

```text
main
```

建议开启：

- Restrict deletions
- Block force pushes
- Require a pull request before merging
- Required approvals：1
- Dismiss stale approvals
- Require review from Code Owners
- Require status checks to pass
- Require branches to be up to date
- Require conversation resolution
- Require linear history

Required status checks：

```text
Quality
Tests / Python 3.10
Tests / Python 3.11
Tests / Python 3.12
Tests / Python 3.13
PyTorch CPU
Build package
Validate Conventional Commit title
Analyze Python
```

允许的合并方式建议仅保留：

```text
Squash merging
```

## develop 规则

目标分支：

```text
develop
```

建议与 `main` 基本相同，但可以不要求 Code Owner，仍然要求：

- Pull Request
- 1 个批准
- CI 状态检查
- 分支保持最新
- 禁止强制推送
- 禁止删除

## release/* 与 hotfix/*

建议禁止强制推送和删除，不强制要求审批，便于维护者做版本整理。
