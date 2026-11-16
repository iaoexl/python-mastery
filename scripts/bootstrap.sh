#!/usr/bin/env bash
# 项目完整性第「1」步：从一个空目录开始，建文件夹、写第一个文件、跑通、打包发布。
# 它验证的是"照着知识库板块1 能不能真的起个项目"，不是复刻主工程。
# 用法：bash scripts/bootstrap.sh [目标空目录]；缺省落到临时目录。
set -euo pipefail

PY="${PYTHON:-python}"
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
TARGET="${1:-/tmp/records_bootstrap}"
CACHE_ROOT="${CACHE_ROOT:-/tmp/records_boot_cache}"

# 清空前的护栏：拒绝根目录、家目录、仓库本身，并要求目标落在 /tmp 或仓库子目录内。
case "$TARGET" in
  ""|"/"|"."|".."|"$HOME"|"$HOME"/*|"$REPO") echo "拒绝清空危险路径: $TARGET" >&2; exit 1 ;;
esac
if [ -d "$TARGET" ]; then
  TARGET="$(cd "$TARGET" && pwd)"
else
  TARGET_PARENT="$(dirname "$TARGET")"
  [ -d "$TARGET_PARENT" ] || { echo "父目录不存在: $TARGET" >&2; exit 1; }
  TARGET="$(cd "$TARGET_PARENT" && pwd)/$(basename "$TARGET")"
fi
case "$TARGET" in
  /tmp/*|"$REPO"/*) ;;
  *) echo "目标须在 /tmp 或仓库子目录内: $TARGET" >&2; exit 1 ;;
esac

mkdir -p "$CACHE_ROOT"
export COVERAGE_FILE="$CACHE_ROOT/.coverage"

if ! "$PY" -c "import build, pytest, setuptools, wheel" >/dev/null 2>&1; then
  local_err="$CACHE_ROOT/pip-install.err"
  if ! "$PY" -m pip install -q -r "$HERE/../requirements.lock" 2>"$local_err"; then
    if grep -qi "externally-managed-environment" "$local_err"; then
      echo "宿主 Python 受 PEP 668 保护；请用自建虚拟环境的解释器重跑" >&2
    else
      cat "$local_err" >&2
    fi
    exit 1
  fi
  echo "toolchain bootstrapped from requirements.lock"
fi

rm -rf "$TARGET"
mkdir -p "$TARGET"
cd "$TARGET"

# 演示项目装进它自己的隔离环境，不污染宿主解释器。
"$PY" -m venv --without-pip --system-site-packages .venv
BOOT_PY=.venv/bin/python
if [ ! -x "$BOOT_PY" ]; then BOOT_PY=.venv/Scripts/python.exe; fi

echo "== 第1步 空目录与文件夹安排 =="
mkdir -p src/hello_pkg tests scripts dist
cat > 目录安排.md <<'EOF'
# 目录安排（起步版）

| 路径 | 解决什么 | 放错的后果 |
| --- | --- | --- |
| `pyproject.toml` | 项目声明与构建后端 | 只留宽松版本声明，机器无法复现 |
| `src/hello_pkg/` | 已安装形态与源树隔离 | 靠脚本目录碰巧可导入，打包后子包消失 |
| `tests/` | 用例与实现分离 | 测试跟着源码一起被发出去 |
| `scripts/` | 门禁、快照、演练脚本 | 环境步骤不可复跑 |
| `dist/`（不入库） | 打包发布产物 | 产物混进版本库 |
| `.venv/`（不入库） | 演示项目的隔离环境 | 装进宿主解释器会污染全局包集合 |
EOF
echo "  已建 src/hello_pkg、tests、scripts、dist、.venv，并写下目录安排.md"

echo "== 第2步 第一个文件：pyproject.toml =="
cat > pyproject.toml <<'EOF'
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "hello-pkg"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = []

[tool.setuptools.packages.find]
where = ["src"]
EOF
cat > README.md <<'EOF'
# hello-pkg（起步版）

从空目录建起的第一个可分发项目：一个纯函数、一条用例、一份目录安排。
EOF
test -s pyproject.toml && grep -q '^name = "hello-pkg"' pyproject.toml
echo "  项目声明与说明文件就位"

echo "== 第3步 第二个文件：包内第一个模块 =="
cat > src/hello_pkg/__init__.py <<'EOF'
"""起步包：顶层只放定义，不放有副作用的启动逻辑。"""


def word() -> str:
    """第一个可测的纯函数。"""
    return "hello"
EOF
cat > tests/test_word.py <<'EOF'
from hello_pkg import word


def test_word():
    assert word() == "hello"
EOF
echo "  包内模块与用例各就位"

echo "== 第4步 第一次跑通（按已安装形态，不靠脚本目录）=="
"$BOOT_PY" -m pip install -q --no-build-isolation -e .
"$BOOT_PY" -c "from hello_pkg import word; assert word() == 'hello'; print('import ok')"
"$BOOT_PY" -m pytest -q
"$BOOT_PY" -m compileall -q src tests
echo "  导入、测试、语法检查全绿（在目标目录自己的 .venv 内）"

echo "== 第5步 打包发布 =="
"$BOOT_PY" -m build --no-isolation --outdir dist >/dev/null
WHEEL="$(find dist -maxdepth 1 -type f -name '*.whl' -print -quit || true)"
if [ -z "$WHEEL" ]; then echo "未产出 wheel" >&2; exit 1; fi
META=$("$BOOT_PY" -c "
import zipfile, sys
with zipfile.ZipFile(sys.argv[1]) as z:
    n = [x for x in z.namelist() if x.endswith('METADATA')][0]
    print([l for l in z.read(n).decode().splitlines() if l.startswith('Name:')][0])
" "$WHEEL")
echo "  $META"
cp 目录安排.md dist/目录安排.md
cat > dist/发布清单.md <<'EOF'
# 发布清单（起步版）

| 项 | 内容 |
| --- | --- |
| 产物 | 分发压缩包，由 `build --no-isolation` 生成 |
| 元数据 | 压缩包内 METADATA 可读出项目名 |
| 源码边界 | `dist/` 不入库，只交付产物与清单 |
| 复跑 | `python -m build --no-isolation --outdir dist` |
EOF
echo "  产物、元数据、发布清单齐备"

echo "== 判定 =="
echo "空目录起步：通过；文件夹安排：通过；第一个文件可跑：通过；打包发布：通过"
echo "BOOTSTRAP_PASSED"
