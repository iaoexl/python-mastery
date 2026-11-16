#!/usr/bin/env bash
# 12_5「故障演练与回滚」的本地实物载体。
# 演完整半程：两个不同版本的分发产物 -> 两份独立安装副本 -> 新版本处理一组输入
# -> 按指针切回旧版本 -> 逐条比对 -> 旧版本副本上复跑门禁。
# 判定看三件事：版本可辨识、指针真正驱动生效路径、同一组输入输出一致。
# 线上多实例切换仍属部署侧，见 0_2 边界声明。
set -euo pipefail
cd "$(dirname "$0")/.."
REPO="$(pwd)"

PY="${PYTHON:-python}"
CACHE_ROOT="${CACHE_ROOT:-/tmp/records_cache}"
export COVERAGE_FILE="$CACHE_ROOT/.coverage"
mkdir -p "$CACHE_ROOT"

if ! "$PY" -c "import build" >/dev/null 2>&1; then
  local_err="$CACHE_ROOT/pip-install.err"
  if ! "$PY" -m pip install -q -r requirements.lock 2>"$local_err"; then
    if grep -qi "externally-managed-environment" "$local_err"; then
      echo "宿主 Python 受 PEP 668 保护；请用自建虚拟环境的解释器重跑" >&2
    else
      cat "$local_err" >&2
    fi
    exit 1
  fi
  echo "toolchain bootstrapped"
fi

WORK="${DRILL_WORK:-/tmp/records_rollback}"
case "$WORK" in
  ""|"/"|"."|".."|"$HOME"|"$HOME"/*|"$REPO") echo "拒绝清空危险路径: $WORK" >&2; exit 1 ;;
esac
if [ -d "$WORK" ]; then
  WORK="$(cd "$WORK" && pwd)"
else
  WORK_PARENT="$(dirname "$WORK")"
  [ -d "$WORK_PARENT" ] || { echo "父目录不存在: $WORK" >&2; exit 1; }
  WORK="$(cd "$WORK_PARENT" && pwd)/$(basename "$WORK")"
fi
case "$WORK" in
  /tmp/*|"$REPO"/*) ;;
  *) echo "演练目录须在 /tmp 或仓库子目录内: $WORK" >&2; exit 1 ;;
esac

rm -rf "$WORK"
mkdir -p "$WORK/dist" "$WORK/prev_dist" "$WORK/prev_src" "$WORK/v_prev" "$WORK/v_curr"

echo "== 第1步 构建两个不同版本的分发产物 =="
"$PY" -m build --no-isolation --outdir "$WORK/dist" >/dev/null
CURR_WHEEL="$(find "$WORK/dist" -maxdepth 1 -type f -name 'records_atlas-0.1.0-*.whl' -print -quit || true)"
[ -n "$CURR_WHEEL" ] || { echo "未产出当前版本 wheel" >&2; exit 1; }

cp pyproject.toml LICENSE "$WORK/prev_src/"
cp -R src "$WORK/prev_src/"
"$PY" - "$WORK/prev_src/pyproject.toml" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
assert 'version = "0.1.0"' in s, "主工程版本已变，需同步演练脚本的基准版本"
p.write_text(s.replace('version = "0.1.0"', 'version = "0.0.1"', 1), encoding="utf-8", newline="\n")
PY
(cd "$WORK/prev_src" && "$PY" -m build --no-isolation --outdir "$WORK/prev_dist" >/dev/null)
PREV_WHEEL="$(find "$WORK/prev_dist" -maxdepth 1 -type f -name 'records_atlas-0.0.1-*.whl' -print -quit || true)"
[ -n "$PREV_WHEEL" ] || { echo "未产出旧版本 wheel" >&2; exit 1; }
echo "  当前版本 $(basename "$CURR_WHEEL")"
echo "  旧版本   $(basename "$PREV_WHEEL")"

echo "== 第2步 装出两份独立副本，验版本可辨识 =="
"$PY" -m pip install -q --no-deps --target "$WORK/v_prev" "$PREV_WHEEL"
"$PY" -m pip install -q --no-deps --target "$WORK/v_curr" "$CURR_WHEEL"
check_meta() {
  local dir="$1" want="$2" meta
  meta="$(find "$dir" -maxdepth 2 -type f -path '*/records_atlas-*.dist-info/METADATA' -print -quit || true)"
  [ -n "$meta" ] || { echo "元数据缺失: $dir" >&2; exit 1; }
  grep -q '^Name: records-atlas' "$meta" || { echo "元数据不可读: $dir" >&2; exit 1; }
  grep -q "^Version: $want" "$meta" || { echo "版本不符（期望 $want）: $dir" >&2; exit 1; }
  echo "  $dir 版本 $want 可辨识"
}
check_meta "$WORK/v_prev" 0.0.1
check_meta "$WORK/v_curr" 0.1.0

target_for() {
  case "$1" in
    prev) printf '%s' "$WORK/v_prev" ;;
    curr) printf '%s' "$WORK/v_curr" ;;
    *) echo "未知指针值: $1" >&2; exit 1 ;;
  esac
}

run_suite() {
  local target="$1" out="$2"
  PYTHONPATH="$target" "$PY" - "$WORK/state" > "$out" <<'PY'
import sys
from records.core import parse_batch, parse_spec
with open(sys.argv[1], encoding="utf-8") as fh:
    lines = [line.rstrip("\n") for line in fh]
for line in lines:
    print("spec", repr(line), "->", parse_spec(line))
print("batch ->", parse_batch(["a:1", "bad", "b:2"]))
PY
}

echo "== 第3步 新版本处理一组输入 =="
printf 'a:7\nb:3\n  c : 11 \nsingle\n' > "$WORK/state"
echo curr > "$WORK/current"
CURRENT="$(cat "$WORK/current")"
[ "$CURRENT" = "curr" ] || { echo "指针未指向新版本" >&2; exit 1; }
TARGET="$(target_for "$CURRENT")"
echo "  生效路径 $TARGET"
PYTHONPATH="$TARGET" "$PY" -c "from importlib.metadata import version; print('  运行时版本', version('records-atlas'))"
run_suite "$TARGET" "$WORK/curr.out"
echo "  curr 输出 $(wc -l < "$WORK/curr.out") 行"

echo "== 第4步 切回旧版本，重放并比对 =="
echo prev > "$WORK/current"
CURRENT="$(cat "$WORK/current")"
TARGET="$(target_for "$CURRENT")"
[ "$TARGET" = "$WORK/v_prev" ] || { echo "指针未真正回退到旧版本路径" >&2; exit 1; }
echo "  生效路径 $TARGET"
PYTHONPATH="$TARGET" "$PY" -c "from importlib.metadata import version; print('  运行时版本', version('records-atlas'))"
run_suite "$TARGET" "$WORK/prev.out"
if ! diff -u "$WORK/curr.out" "$WORK/prev.out" >/dev/null; then
  echo "回滚后输出不一致" >&2
  diff -u "$WORK/curr.out" "$WORK/prev.out" | head -n 20 >&2
  exit 1
fi
echo "  指针回退，逐条输出一致"

echo "== 第5步 旧版本副本上复跑门禁 =="
"$PY" -m compileall -q "$WORK/v_prev/records"
if ! PYTHONPATH="$WORK/v_prev" "$PY" -m pytest -o addopts="" -q > "$WORK/pytest.log" 2>&1; then
  cat "$WORK/pytest.log" >&2
  exit 1
fi
tail -n 3 "$WORK/pytest.log"
PASSED="$(grep -Eo '[0-9]+ passed' "$WORK/pytest.log" | tail -n 1 || true)"
[ -n "$PASSED" ] || { echo "未读到用例通过数量" >&2; exit 1; }

echo "== 判定 =="
echo "版本可辨识：通过；指针驱动生效路径：通过；同一组输入输出一致：通过；旧版本副本门禁复跑：$PASSED"
echo "ROLLBACK_DRILL_PASSED"
