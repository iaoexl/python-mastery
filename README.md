# Python 语言从入门到精通（python-mastery）

[![文档: CC BY 4.0](https://img.shields.io/badge/Docs-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/deed.zh)
[![代码: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)

作者：iaoexl

> 一套能读、能跑、能复验的 Python 教程工程：`docs/` 讲机理，`src/` 与 `tests/` 把机理写成可验证的实现，五个 `scripts/` 脚本把环境、门禁、重建、回滚、起步串成可重跑的命令。
>
> 本仓库不是语法速查表。它按「代码被写出来 → 被读懂对象模型 → 被抽象 → 被并发调度 → 被测试 → 被交付」的顺序推进，每个板块都配操作清单、笔记方法和判定动作。包名是 `records-atlas`，见 `pyproject.toml`。

第一次来：先读 `docs/分板块/README.md` 的板块地图与三级刻度，按「快速开始」跑一遍 `baseline.sh` 与 `check.sh`，再照「目录与板块对应」表挑一个板块动手。

## 内容地图

| 路径 | 里面是什么 | 什么时候用 |
| --- | --- | --- |
| `docs/Python语言从入门到精通.md` | 全册合订稿，含 README_1 至 README_8 导览 | 通读、按概念检索 |
| `docs/分板块/README.md` | 板块地图、记号约定、按症状反查表、三级能力刻度 | 决定读哪一块、卡住时反查 |
| `docs/分板块/` 下的 `00`—`12` | 13 个板块文件；自板块1 起每块六节（X_1 机理、X_2 操作、X_3 笔记法、X_4 案例、X_5 验证、X_6 误区） | 逐块动手 |
| `src/records/` | `core.py`、`boundary.py`、`workers.py`、`__init__.py`；顶层只放定义，不放启动逻辑 | 对照机理读实现 |
| `tests/` | 三个测试文件与 `conftest.py`；函数级 fixture 每次新建，会话级只返回不可变元组 | 验证机理、保留反例 |
| `scripts/` | `baseline.sh`、`check.sh`、`rebuild_clean.sh`、`rollback_drill.sh`、`bootstrap.sh` | 换环境、验门禁、做演练 |
| `pyproject.toml` / `requirements.lock` | 前者含 SPDX 许可声明 `MIT`，后者锁给机器复现 | 干净重建、产物元数据核对 |
| `LICENSE` | 文档与代码的分层许可、AI 生成声明与权利边界 | 引用、二创、商用前 |

## 快速开始

前置：Python 3.9 及以上、可运行 bash 的终端（Windows 用 Git Bash）。命令都在仓库根目录执行，不需要先 `cd` 到别的文件夹。

```bash
bash scripts/baseline.sh          # 环境归因：解释器身份、sys.path 首位、隔离开关、导入耗时
bash scripts/check.sh             # 分层门禁（L-1 至 L4），末行 ALL_GATES_PASSED 才算通过
bash scripts/rebuild_clean.sh     # 干净环境重建，末行 CLEAN_REBUILD_PASSED 才算通过
bash scripts/rollback_drill.sh    # 回滚演练，末行 ROLLBACK_DRILL_PASSED 才算通过
bash scripts/bootstrap.sh /tmp/新项目   # 空目录起步，末行 BOOTSTRAP_PASSED 才算通过
```

`check.sh` 用 `--system-site-packages` 复用宿主工具链以便快速复跑；`rebuild_clean.sh` 用独立环境创建工具按 `requirements.lock` 从零安装，不复用宿主站点包。两条路线的输出判定一致才算可复现。缺工具时脚本会按锁文件自举。

| 脚本 | 通过标记 | 会改动的目录 |
| --- | --- | --- |
| `baseline.sh` | 无标记，输出供人工贴进场景卡 | 只读 |
| `check.sh` | `ALL_GATES_PASSED` | `.venv/`、`dist/`、`CACHE_ROOT` |
| `rebuild_clean.sh` | `CLEAN_REBUILD_PASSED` | `CLEAN_VENV`、`CLEAN_DIST`、`CACHE_ROOT` |
| `rollback_drill.sh` | `ROLLBACK_DRILL_PASSED` | `DRILL_WORK`、`CACHE_ROOT` |
| `bootstrap.sh` | `BOOTSTRAP_PASSED` | 传入的目标目录、`CACHE_ROOT` |

注意：`bootstrap.sh`、`rebuild_clean.sh`、`rollback_drill.sh` 都会先清空各自的目标目录。运行前对照下表确认路径，别把目标指向有内容的目录。解释器可用 `PYTHON` 指定。

| 变量 / 参数 | 默认值 | 使用脚本 |
| --- | --- | --- |
| `CACHE_ROOT` | `/tmp/records_cache` | `check.sh`、`rollback_drill.sh` |
| `CACHE_ROOT` | `/tmp/records_cache_clean` | `rebuild_clean.sh` |
| `CACHE_ROOT` | `/tmp/records_boot_cache` | `bootstrap.sh` |
| `CLEAN_VENV` | `/tmp/records_clean_venv` | `rebuild_clean.sh` |
| `CLEAN_DIST` | `/tmp/records_dist_clean` | `rebuild_clean.sh` |
| `DRILL_WORK` | `/tmp/records_rollback` | `rollback_drill.sh` |
| `TARGET`（位置参数） | `/tmp/records_bootstrap` | `bootstrap.sh` |

## 目录与板块对应

表中编号指 `docs/分板块/` 内的小节号，例如 `3_1` 是板块3 的 X_1 核心机理，`9_5` 是板块9 的 X_5 实用验证。

| 路径 | 对应板块 | 可验证的机理 |
| --- | --- | --- |
| `pyproject.toml`、`requirements.lock` | 0_3、6_1 | 项目声明、构建后端、包发现、依赖锁定、SPDX 许可字段 |
| `src/records/core.py` | 2_1、3_1、4_1、7_1 | 名称绑定、可变默认参数、共享默认值、深浅拷贝、`Decimal` 金额、异常留痕、反序列化红线 |
| `src/records/boundary.py` | 11_1 | 配置四级优先、错误分类、退避抖动、幂等键、四种降级形态、存活/就绪两分探针、结构化日志 |
| `src/records/workers.py` | 8_1、8_4 | `as_completed` 按完成顺序、`result()` 回收异常、死信列表 |
| `src/records/__init__.py` | 6_1 | 按模块名导出，顶层不放有副作用的启动逻辑 |
| `tests/conftest.py` | 9_1 | 函数级每次新建，会话级只放不可变对象 |
| `tests/test_core.py` | 3_3、9_3 | 参数化、`raises` 的 `match`、近似断言、`memoryview` 共享缓冲、红—绿对照 |
| `tests/test_boundary.py` | 9_3、11_3 | `monkeypatch` 打在被查找处、异常链、预算耗尽、幂等复查 |
| `tests/test_workers.py` | 8_5 | 完成数量不等于结果正确，失败必须进死信列表 |
| `scripts/baseline.sh` | 1_1、1_3 | `prefix` 之差、`sys.path` 首位、隔离开关 |
| `scripts/bootstrap.sh` | 1_1、1_2 | 空目录 → 第一个文件 → 文件夹安排 → 第一次跑通 → 打包发布 |
| `scripts/check.sh` | 9_5、12_5 | 分层门禁与逐项判分 |
| `scripts/rebuild_clean.sh` | 12_5 | 不复用宿主站点包、按锁文件重建、产物元数据核对 |
| `scripts/rollback_drill.sh` | 12_1、12_5 | 双安装副本切换、输入一致性与数据无损 |

`bootstrap.sh` 验证的是「照着板块1 能不能真的起个项目」，不是复刻本工程。它按已安装形态验证导入，不靠脚本目录碰巧可导入；末尾产出分发压缩包、`目录安排.md` 与 `发布清单.md`。

## 红—绿对照

五处改动都能主动让测试变红：

| 改动 | 会变红的用例 |
| --- | --- |
| 把 `parse_spec` 的默认值改回 `extra=[]` | `test_parse_spec_does_not_remember_previous_call` |
| `group_by` 改用 `dict.fromkeys` | `test_group_by_each_key_owns_its_list` |
| `snapshot` 改成切片 | `test_deepcopy_vs_slice_sharing` |
| `fetch_with_retry` 去掉错误分类 | `test_deterministic_failure_is_never_retried` |
| 删掉 `run_all` 里的 `result()` | `test_failure_goes_to_dead_letters_not_silently_dropped`、`test_completion_count_alone_would_hide_the_failure` |

共享默认值一类反模式被显式留在测试里，作为反例清单，不清理掉。删了实现仍全绿的断言是假断言，先修断言再继续。

12_5 的九项判分表不预填、不事后补签。换机器重跑时自己填「现场判定」列，不把别人的「通过」抄进自己的判分表。场景卡模板见各板块 X_3 节，按 12_3 归档自己填好的卡后抽查。

## 协议（文档 CC BY 4.0 · 代码 MIT）

### 协议摘要

> 本仓库按内容类型分层授权：`README.md`、`docs/` 下的教程与说明文字采用 **CC BY 4.0**；`src/`、`tests/`、`scripts/` 下的代码、测试、脚本以及 `pyproject.toml`、`requirements.lock` 采用 **MIT License**。
> 使用者可以复制、改编、商用，两种许可都要求保留署名与许可声明。第三方原始资料不在授权范围内。

分层理由：本仓库同时含教程与可运行代码。知识共享官方 FAQ 明确不建议把 CC 许可用于软件本身，并说明 CC 许可可用于软件文档；代码部分因此使用软件专用许可，文档部分沿用与同类笔记库一致的 CC BY 4.0。

### AI 生成内容声明

> 本仓库的 Markdown 文档、示例代码、测试、脚本与说明文字由 AI 工具依据公开资料与使用者指令生成、归纳与结构化。LICENSE 表达的是「在依法可授权的范围内按对应条款允许使用」；本仓库不判断 AI 生成内容在各法域是否构成受保护作品，也不判断其权属。若某部分依法不受排他权利覆盖，LICENSE 同时视为发布者不就该部分主张排他权利的承诺。

### 完整协议

[CC BY 4.0 知识共享署名 4.0 国际许可协议](https://creativecommons.org/licenses/by/4.0/deed.zh) · [MIT License](https://opensource.org/license/mit) · 分层范围、AI 生成声明与权利边界见仓库根目录 [LICENSE](LICENSE)。

## 使用建议与边界声明

- 内容仅供学习与自我验证参考，不构成生产环境可用性承诺、安全承诺或专业意见。
- Python 官方文档、标准文本、教材、工具书、厂商文档等第三方资料的著作权归各自权利人；本仓库仅对自身编写与整理成果授权。
- 二创与再分发请保留出处和许可声明；商业使用前请自行核查所引第三方资料的合规情况。
- 部分脚本会清空指定目录（见上表「会改动的目录」），运行前确认路径。
- `LICENSE` 里的版权人为 iaoexl，年份为 2026；署名格式、MIT 版权行与 `pyproject.toml` 的 `authors` 字段保持一致。
- 类型检查按 Python 3.10 语法口径执行：当前 mypy 版本不接受把 3.9 设为分析目标；运行时代码通过 `from __future__ import annotations` 兼容 3.9。

## 资料来源（MLA 格式）

Creative Commons. "Frequently Asked Questions." *CC Public Wiki*, wiki.creativecommons.org/wiki/FAQ. Accessed 16 Nov. 2026.

Creative Commons. "Attribution 4.0 International (CC BY 4.0)." *Creative Commons*, creativecommons.org/licenses/by/4.0/deed.zh. Accessed 16 Nov. 2026.

Open Source Initiative. "MIT License." *Open Source Initiative*, opensource.org/license/mit. Accessed 16 Nov. 2026.

## 请我喝杯咖啡

|     微信赞赏码     |       支付宝        |       支付宝红包        |
| :----------------: | :-----------------: | :-----------------: |
| <img src="images/wx.jpg" alt="赞赏码" width="200"> | <img src="images/zfb.jpg" alt="支付宝" width="200">| <img src="images/zfb_hb.jpg" alt="支付宝红包" width="200">|

## 你可以在这些地方找到我 (Find Me Here)

<p align="center">
  <a href="https://gitcode.com/iaoexl/python-mastery.git" target="_blank" rel="noopener">
    <img src="images/favicon_gitcode.ico" width="18" height="18" alt="GitCode">&nbsp;GitCode
  </a>
  <span style="color: #999;">&nbsp;/&nbsp;</span>
  <a href="https://atomgit.com/iaoexl/python-mastery.git" target="_blank" rel="noopener">&nbsp;AtomGit
  </a>
  &nbsp;&nbsp;
  <a href="https://cnb.cool/iaoexl/python-mastery.git" target="_blank" rel="noopener">
    <img src="images/favicon_cnb.ico" width="18" height="18" alt="腾讯云 CNB">&nbsp;腾讯云 CNB
  </a>
  &nbsp;&nbsp;
  <a href="https://gitee.com/iaoexl/python-mastery.git" target="_blank" rel="noopener">
    <img src="images/favicon_gitee.ico" width="18" height="18" alt="Gitee">&nbsp;Gitee
  </a>
  &nbsp;&nbsp;
  <a href="https://github.com/iaoexl/python-mastery.git" target="_blank" rel="noopener">
    <img src="images/favicon_github.png" width="18" height="18" alt="GitHub">&nbsp;GitHub
  </a>
</p>