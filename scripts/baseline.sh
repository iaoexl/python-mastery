#!/usr/bin/env bash
# 环境快照卡用：原样贴输出，判定看的是 prefix 之差与 sys.path 首位，不是提示符里的括号。
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${PYTHON:-python}"
echo "--- version ---";                 "$PY" --version
echo "--- identity ---";
"$PY" -c "import sys; print('prefix',sys.prefix); print('base_prefix',sys.base_prefix)"
"$PY" -c "import sys; print('executable',sys.executable)"
echo "--- sys.path[0] 三种启动 ---";
"$PY" -c "import sys; print('script-like first:', sys.path[0] or '(empty)')"
"$PY" -I -c "import sys; print('isolated first:', sys.path[0] or '(empty)')"
"$PY" - <<'PY'
import os, pathlib, shutil, subprocess, sys, tempfile
probe_dir = tempfile.mkdtemp()
try:
    pathlib.Path(probe_dir, "pathprobe.py").write_text(
        'import sys; print("module-style first:", sys.path[0] or "(empty)")\n', encoding="utf-8"
    )
    env = dict(os.environ, PYTHONPATH=probe_dir)
    subprocess.run([sys.executable, "-m", "pathprobe"], env=env, check=True)
finally:
    shutil.rmtree(probe_dir, ignore_errors=True)
PY
"$PY" -c "import sys; print('path entries:', len(sys.path))"
echo "--- 隔离开关可用性 ---";
"$PY" -E -c "print('E ok')" && "$PY" -S -c "print('S ok')"
echo "--- 导入耗时最慢层 ---";
PYTHONPATH=src "$PY" -X importtime -c "import records" 2>&1 | tail -n 4
echo "--- 按包方式启动入口 ---";
PYTHONPATH=src "$PY" -c "from records.core import parse_spec; print(parse_spec('a:1'))"
