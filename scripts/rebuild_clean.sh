#!/usr/bin/env bash
# 12_5 判分表"干净环境重建"一项的实测载体：不复用宿主站点包，按锁文件从零安装。
# 环境本体与产物落到临时目录：某些工作区卷对"递归删非空目录"与 sqlite 写不友好，
# 换落点即可，判定口径（隔离前缀、按锁文件、同命令重跑）一律不变。
set -euo pipefail
cd "$(dirname "$0")/.."
REPO="$(pwd)"

PY="${PYTHON:-python}"
CACHE_ROOT="${CACHE_ROOT:-/tmp/records_cache_clean}"
VENVDIR="${CLEAN_VENV:-/tmp/records_clean_venv}"
DIST="${CLEAN_DIST:-/tmp/records_dist_clean}"
mkdir -p "$CACHE_ROOT"
export COVERAGE_FILE="$CACHE_ROOT/.coverage"
MYPY_CACHE="$CACHE_ROOT/mypy"

# 清空前的护栏：拒绝根目录、家目录、仓库本身，并要求目标落在 /tmp 或仓库子目录内。
guard_rm() {
  local raw="$1" abs parent base
  case "$raw" in
    ""|"/"|"."|".."|"$HOME"|"$HOME"/*) echo "拒绝清空危险路径: $raw" >&2; exit 1 ;;
  esac
  if [ -d "$raw" ]; then
    abs="$(cd "$raw" && pwd)"
  else
    parent="$(dirname "$raw")" base="$(basename "$raw")"
    [ -d "$parent" ] || { echo "父目录不存在: $raw" >&2; exit 1; }
    abs="$(cd "$parent" && pwd)/$base"
  fi
  case "$abs" in
    "/"|"$HOME"|"$HOME"/*|"$REPO") echo "拒绝清空危险路径: $abs" >&2; exit 1 ;;
  esac
  case "$abs" in
    /tmp/*|"$REPO"/*) ;;
    *) echo "目标须在 /tmp 或仓库子目录内: $abs" >&2; exit 1 ;;
  esac
  printf '%s' "$abs"
}

SAFE_VENV="$(guard_rm "$VENVDIR")"
SAFE_DIST="$(guard_rm "$DIST")"

if ! "$PY" -c "import virtualenv" >/dev/null 2>&1; then
  local_err="$CACHE_ROOT/pip-install.err"
  if ! "$PY" -m pip install -q -r requirements.lock 2>"$local_err"; then
    if grep -qi "externally-managed-environment" "$local_err"; then
      echo "宿主 Python 受 PEP 668 保护；请用自建虚拟环境的解释器重跑" >&2
    else
      cat "$local_err" >&2
    fi
    exit 1
  fi
fi

rm -rf "$SAFE_VENV" "$SAFE_DIST"
"$PY" -m virtualenv --no-download "$SAFE_VENV"
CLEAN="$SAFE_VENV/bin/python"
if [ ! -x "$CLEAN" ]; then CLEAN="$SAFE_VENV/Scripts/python.exe"; fi

echo "== 身份：不得与宿主共用前缀 =="
"$CLEAN" -c "import sys; assert sys.prefix != sys.base_prefix; print('isolated prefix ok')"

echo "== 按锁文件安装并以已安装形态验证 =="
"$CLEAN" -m pip install -q -r requirements.lock
"$CLEAN" -m pip install -q --no-build-isolation -e .
"$CLEAN" -m pip check
"$CLEAN" -c "import records; print('installed import ok')"

echo "== 在干净环境重跑门禁 =="
"$CLEAN" -m pytest -q --durations=5
"$CLEAN" -m pytest -q tests/test_workers.py tests/test_boundary.py tests/test_core.py
"$CLEAN" -m pytest --cov=records --cov-report=term-missing -q
"$CLEAN" -m mypy --cache-dir="$MYPY_CACHE" src
"$CLEAN" -m compileall -q src tests
"$CLEAN" -m ruff check src tests

echo "== 产物元数据 =="
"$CLEAN" -m build --outdir "$SAFE_DIST" --no-isolation >/dev/null
WHEEL="$(find "$SAFE_DIST" -maxdepth 1 -type f -name '*.whl' -print -quit 2>/dev/null || true)"
if [ -z "$WHEEL" ]; then echo "干净环境未产出 wheel" >&2; exit 1; fi
echo "wheel built in clean env: $(basename "$WHEEL")"

echo "CLEAN_REBUILD_PASSED"
