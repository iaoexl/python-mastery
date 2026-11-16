#!/usr/bin/env bash
# 分层门禁：L-1 工具前提 / L0 隔离环境 / L1 语法与依赖 / L2 测试 / L3 覆盖与类型 / L4 构建
# 环境若未提供 ensurepip，用 --without-pip 建环境、由 system-site-packages 暴露工具链；
# 真正的"不复用宿主站点包"重建另见 rebuild_clean.sh。
# 覆盖率数据文件与 mypy 缓存放到临时目录：某些工作区卷对 sqlite 并发写不友好，
# 会出现 disk I/O error，换落点即可，不影响判定口径。
set -euo pipefail
cd "$(dirname "$0")/.."
REPO="$(pwd)"

PY="${PYTHON:-python}"
CACHE_ROOT="${CACHE_ROOT:-/tmp/records_cache}"
mkdir -p "$CACHE_ROOT"
export COVERAGE_FILE="$CACHE_ROOT/.coverage"
MYPY_CACHE="$CACHE_ROOT/mypy"

install_tools() {
  local err="$CACHE_ROOT/pip-install.err"
  if ! "$PY" -m pip install -q -r requirements.lock 2>"$err"; then
    if grep -qi "externally-managed-environment" "$err"; then
      echo "宿主 Python 受 PEP 668 保护；请用自建虚拟环境的解释器重跑：PYTHON=/path/to/venv/bin/python bash $0" >&2
    else
      cat "$err" >&2
    fi
    exit 1
  fi
  echo "toolchain bootstrapped from requirements.lock"
}

require_wheel() {
  local dir="$1" wheel
  wheel="$(find "$dir" -maxdepth 1 -type f -name '*.whl' -print -quit 2>/dev/null || true)"
  if [ -z "$wheel" ]; then echo "未产出分发压缩包: $dir" >&2; exit 1; fi
  echo "wheel built: $(basename "$wheel")"
}

echo "== L-1 工具前提（见 0_3 基线表）=="
if ! "$PY" -c "import pytest, coverage, mypy, build, ruff" >/dev/null 2>&1; then
  install_tools
else
  echo "toolchain present"
fi

"$PY" -m venv --without-pip --system-site-packages .venv
VENV_PY=.venv/bin/python
if [ ! -x "$VENV_PY" ]; then VENV_PY=.venv/Scripts/python.exe; fi

echo "== L0 隔离环境与解释器身份 =="
"$VENV_PY" -c "import sys; assert sys.prefix != sys.base_prefix; print('prefix ok')"

echo "== L1 语法、格式、导入与依赖冲突 =="
"$VENV_PY" -m pip check
"$VENV_PY" -m compileall -q src tests
"$VENV_PY" -m ruff check src tests
PYTHONPATH=src "$VENV_PY" -c "import records; print('package import ok')"

echo "== L2 测试与耗时观察（两种收集顺序）=="
PYTHONPATH=src "$VENV_PY" -m pytest -q --durations=5
PYTHONPATH=src "$VENV_PY" -m pytest -q tests/test_workers.py tests/test_boundary.py tests/test_core.py

echo "== L3 覆盖率、薄弱行与类型检查 =="
PYTHONPATH=src "$VENV_PY" -m pytest --cov=records --cov-report=term-missing -q
"$VENV_PY" -m mypy --cache-dir="$MYPY_CACHE" src

echo "== L4 干净构建产物 =="
"$VENV_PY" -m build --no-isolation --outdir dist >/dev/null
require_wheel dist

echo "ALL_GATES_PASSED"
