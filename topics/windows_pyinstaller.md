# PyInstaller 打包指南

> 本机环境：Windows；Python 3.10.0rc2（`C:\Program Files\Python310\python.exe`）；PyInstaller 6.16.0。
> 内容包括安装、输出结构、常用参数、资源文件、排错与发布注意事项。

## 1. 安装与版本确认

安装命令：

```bat
pip install pywin32
pip install pyinstaller
```

建议用 `python -m pip` 指定解释器，避免装到别的 Python 环境：

```bat
"C:\Program Files\Python310\python.exe" -m pip install pyinstaller
"C:\Program Files\Python310\python.exe" -m PyInstaller --version
```

`pywin32` 只在脚本调用 Windows 特有 API（注册表、服务、COM、进程管理）时才需要，不是打包本身的依赖。普通控制台或图形程序跳过它即可。

## 2. 基本用法与输出

基本示例：

```bat
pyinstaller -F main.py
pyinstaller -F -i icon\logo.ico main.py
```

执行后默认在本目录生成三样东西：

| 输出 | 内容 |
| --- | --- |
| `main.spec` | 打包配置脚本。首次构建时生成，之后 `pyinstaller main.spec` 会直接按它构建；改参数或改文件后若不更新它，改动可能不生效 |
| `build/` | 临时工作文件、日志、`.pyz` 等，可删除 |
| `dist/main.exe` | 交付给用户的可执行文件 |

`-F` 生成单文件 exe；不加 `-F` 时走默认的 `-D` 单目录模式，产物在 `dist/main/`。从 PyInstaller 6.3.0 起，单目录模式默认把 exe 之外的依赖放进 `dist/main/_internal/`，只有 exe 留在 `dist/main/` 根目录。旧脚本若写成 `os.path.dirname(sys.executable)` 去找随包资源，升级后会失效；改用 `__file__` 或 `sys._MEIPASS`。需要旧布局时加 `--contents-directory .`。

## 3. 常用参数

| 参数 | 作用 | 使用时机 |
| --- | --- | --- |
| `-F`, `--onefile` | 把所有内容压进一个可执行文件 | 需要单文件发布时；启动会比单目录模式慢 |
| `-D`, `--onedir` | 生成一个文件夹，里面有 exe 和依赖（默认） | 调试打包问题、需要快速启动时 |
| `-w`, `--windowed`, `--noconsole` | 不显示控制台窗口 | 图形界面程序；命令行程序不要加 |
| `-c`, `--console` | 保留控制台窗口（默认） | 需要看 `print`、报错、`input()` 时 |
| `-i FILE.ico`, `--icon` | 设置 exe 图标 | 示例：`pyinstaller -F -i icon\logo.ico main.py` |
| `-p DIR`, `--paths DIR` | 追加导入搜索路径，作用类似 `PYTHONPATH` | 模块不在当前目录、也不在解释器路径里时 |
| `--add-data SOURCE:DEST` | 把数据文件或目录放进包内 | 配置文件、模板、图片等 |
| `--add-binary SOURCE:DEST` | 把二进制文件放进包内 | 额外的 `.dll`、`.so` 等 |
| `--hidden-import MODULE` | 手动声明静态分析发现不到的导入 | 代码用 `__import__()`、`importlib` 动态加载模块时 |
| `--collect-all PACKAGE` | 收集某个包的子模块、数据和二进制文件 | 第三方包资源不全时 |
| `-n NAME`, `--name NAME` | 指定 exe 和 spec 的名称 | 不想用脚本名当程序名时 |
| `--distpath DIR` / `--workpath DIR` | 改输出目录 / 临时目录 | 需要把产物放到指定位置时 |
| `--clean` | 构建前清缓存和临时文件 | 改了依赖或怀疑旧缓存干扰时 |
| `-y`, `--noconfirm` | 覆盖已有输出，不再询问 | 写进构建脚本时 |
| `--version-file FILE` | 写入 Windows 版本资源信息 | 正式发布、需要文件属性里显示版本时 |
| `--uac-admin` | 运行时请求管理员权限 | 仅在程序确实需要时启用 |
| `--runtime-tmpdir PATH` | 指定单文件程序的解压位置 | 系统临时目录受限时 |
| `--contents-directory DIR` | 指定单目录模式放依赖的子目录名（默认 `_internal`）；写成 `.` 恢复旧布局 | 需要固定的依赖目录名，或兼容按旧布局写的代码 |
| `--collect-data MODULE` / `--collect-binaries MODULE` / `--collect-submodules MODULE` | 只收集指定包的数据 / 二进制 / 子模块，比 `--collect-all` 更窄 | 只想补某一类资源，避免把整个包全塞进去 |
| `--copy-metadata PACKAGE` | 把包的元数据复制进包内 | 运行时用 `importlib.metadata` 读版本号等元数据时 |

## 4. 打包数据文件

本机 PyInstaller 6.16.0 的 `--add-data` 用冒号 `:` 分隔来源和目标目录；目标写成 `.` 表示包根目录：

```bat
pyinstaller -F --add-data "config.ini:." main.py
pyinstaller -F --add-data "assets:assets" -i icon\logo.ico main.py
```

> 说明：本机 6.16.0 帮助文本与当前在线文档都写冒号 `:`；有些旧教程写 Windows 用分号 `;`。分隔符以实际安装的 `--help` 输出为准，用错会出现"找不到数据文件"。

代码里定位随包资源，优先用入口脚本的 `__file__`。冻结程序里，引导器会把它设成包内的绝对路径；源码直接运行时，Python 3.9 起 `__file__` 也是绝对路径，所以同一段代码在开发态和打包态都能用：

```python
from pathlib import Path

base = Path(__file__).resolve().parent
config_path = base / 'config.ini'
```

若代码要显式判断"是否运行在冻结程序里"，或要按包内根目录而不是脚本所在目录定位资源，用 `sys._MEIPASS`。它由引导器在打包程序启动时设置：单目录模式指向包内依赖目录（6.3.0 起为 `_internal`），单文件模式指向临时解压目录；源码直接运行时该属性不存在，所以下面的写法保留了回退：

```python
import sys
from pathlib import Path

base = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
config_path = base / 'config.ini'
```

若文件由用户放在 exe 旁边、不随包发布，用 exe 所在目录定位：

```python
import sys
from pathlib import Path

user_file = Path(sys.executable).resolve().parent / 'user-config.ini'
```

## 5. 单文件与单目录怎么选

- 单目录模式排错更容易：所有收集到的文件都能直接看到；依赖不变时，改完代码可以只替换 exe。
- 单文件模式启动稍慢：启动时会把支持文件解压到系统临时目录 `_MEIxxxxxx`，程序退出后删除。
- 单文件程序被强制结束或崩溃时，临时目录可能残留；`--runtime-tmpdir` 可指定位置。
- 官方建议：先用单目录模式把程序跑通，再切单文件。
- PyInstaller 的产物绑定当前操作系统、Python 版本和位数。换系统、换 Python 版本或 32/64 位，都要在目标环境重新打包。

## 6. 常见排错

| 现象 | 处理 |
| --- | --- |
| 打包成功，运行报 `ModuleNotFoundError` | 加 `--hidden-import 模块名`，或检查 `-p` 路径 |
| 运行报找不到 `.ini`、图片、模板 | 用 `--add-data` 带上文件，再检查代码里的路径写法 |
| GUI 程序双击后直接退出，看不到原因 | 先去掉 `-w` 打包一次，让控制台显示报错 |
| 新代码没生效 | 加 `--clean -y` 重新构建，确认运行的是 `dist` 里的 exe |
| 单文件启动慢、被安全软件误报 | 改用 `-D` 单目录模式 |
| 命令行路径含空格或中文 | 参数加英文双引号，尽量用绝对路径 |
| 升级到 PyInstaller 6.3+ 后按 `sys.executable` 找不到随包资源 | 依赖已移进 `_internal/`；改用 `__file__`，或加 `--contents-directory .` 恢复旧布局 |
| 打包时没报错，运行报 `importlib.metadata.PackageNotFoundError` | 加 `--copy-metadata 包名`，元数据不会自动打进包 |
| 单文件 exe 每次启动都被安全软件删除或拦截 | 先用 `-D` 单目录模式验证；正式发布需做代码签名，或用 `--runtime-tmpdir` 固定解压位置 |
| `--add-data` 用了分号却提示参数格式错误 | 当前版本用冒号 `:` 分隔，按 `--help` 输出改 |

## 7. 推荐构建命令

```bat
pyinstaller -F -y --clean -n MyApp -i icon\logo.ico --add-data "config.ini:." main.py
```

构建后按三步验证，再分发：

1. 从命令行运行 `dist\MyApp.exe`，确认 stdout 和报错都能看到；这一步能抓到图形界面模式下被吞掉的错误。
2. 换一个不含源码的目录运行，确认程序没有偷偷依赖当前工作目录里的文件。
3. 用任务管理器或 `Process Explorer` 确认进程退出后没有残留；单文件模式尤其要查临时目录。

确认无误再压缩 `dist` 目录分发。说明文件不会被 PyInstaller 放进包里，README、授权文件、配置模板要单独发送。

`--clean` 只清缓存和临时文件，不会撤销上一次写出的 `dist` 产物；要干净验证，先删除 `build/`、`dist/` 和 `main.spec` 再构建。

## 参考

"Using PyInstaller." *PyInstaller Documentation*, 6.22.3, pyinstaller.org/en/stable/usage.html. Accessed 18 Nov. 2026.

"What PyInstaller Does and How It Does It." *PyInstaller Documentation*, 6.22.3, pyinstaller.org/en/stable/operating-mode.html. Accessed 18 Nov. 2026.

"Run-time Information." *PyInstaller Documentation*, 6.22.3, pyinstaller.org/en/stable/runtime-information.html. Accessed 18 Nov. 2026.

"PyInstaller --help." *PyInstaller*, version 6.16.0, local installation at `C:\Program Files\Python310\Scripts\pyinstaller.exe`, 18 Nov. 2026.

"PyInstaller Changelog." *PyInstaller Documentation*, 6.22.3, pyinstaller.org/en/stable/CHANGES.html. Accessed 19 Nov. 2026.
