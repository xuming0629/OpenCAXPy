#!/usr/bin/env bash
set -euo pipefail

ruff check .
ruff format --check .
pytest --cov=opencaxpy --cov-report=term-missing
python -m build
python -m twine check dist/*
