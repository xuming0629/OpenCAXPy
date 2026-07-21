#!/usr/bin/env bash
set -euo pipefail

REMOTE="${1:-origin}"

current_branch="$(git branch --show-current)"

if [[ "$current_branch" != "main" ]]; then
    git branch -M main
fi

git push -u "$REMOTE" main

if git show-ref --verify --quiet refs/heads/develop; then
    git checkout develop
else
    git checkout -b develop
fi

git push -u "$REMOTE" develop

echo
echo "Git branches initialized:"
echo "  main    - stable release branch"
echo "  develop - integration branch"
echo
echo "Set develop as the default branch in GitHub repository settings."
