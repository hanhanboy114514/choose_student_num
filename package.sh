#!/usr/bin/env bash
# ============================================================
# package.sh —— 打包脚本（Linux / macOS 版）
#
# 仿照 package.bat 编写，参数用法完全一致：
#     ./package.sh --nuitka [--onefile]
#     ./package.sh --pyinstaller [--onefile]
#
# 前置条件：默认已安装 Python3、Nuitka、PyInstaller
#   - Linux 桌面环境还需 Tk 支持：sudo apt install python3-tk
#   - macOS 需安装带 Tk 的 Python（python.org 或 homebrew）
#
# 与 package.bat 的主要差异（Windows 专用参数在 Linux/macOS 上不可用）：
#   - 图标参数：--windows-icon-from-ico  ->  --linux-icon / --macos-app-icon
#   - PyInstaller --add-data 分隔符：Windows 为 ';'，Linux/macOS 为 ':'
#   - 删除 --windows-console-mod=disable（仅 Windows 有效，非 GUI 窗口参数）
#   - 清理项 choose.exe 对应改为 choose.bin（Nuitka 在 Linux/macOS 上的输出名）
#
# 若提示权限不足，请先执行：chmod +x package.sh
# ============================================================

set -euo pipefail

# 切换到脚本所在目录，保证相对路径与 package.bat 一致
cd "$(dirname "${BASH_SOURCE[0]}")"

# 图标路径（如需更换图标改这里即可；Linux 下若 Nuitka 不支持 .ico 可换成 .png）
ICON="./assets/favicon.png"

# ---------- 清理上次构建产物（对应 package.bat 第 2~9 行） ----------
rm -rf "dist" "build" "choose.onefile-build" "choose.build" "choose.dist" "__pycache__"
rm -f "choose.spec" "choose.exe" "choose.bin"

# ---------- 选择 Python 命令（Linux 上通常为 python3，macOS 亦以 python3 为主） ----------
PYTHON="python3"
command -v python3 >/dev/null 2>&1 || PYTHON="python"

# ---------- 图标参数（数组形式，路径含空格也安全） ----------
# 注意：Nuitka 在 macOS / Linux 上的图标参数名不同，PyInstaller 则统一为 --icon
ICON_OPTS=()
if [ -f "$ICON" ]; then
    case "$(uname -s)" in
        Darwin) ICON_OPTS=("--macos-app-icon=$ICON") ;;
        Linux)  ICON_OPTS=("--linux-icon=$ICON") ;;
        *)      echo "警告：无法识别的系统 $(uname -s)，本次打包将跳过图标参数" ;;
    esac
else
    echo "警告：未找到图标 $ICON，本次打包将跳过图标参数"
fi

case "${1:-}" in
    --nuitka)
        # 检查 Nuitka 是否可用（默认已安装，仅作友好提示）
        if ! "$PYTHON" -m nuitka --version >/dev/null 2>&1; then
            echo "错误：未找到 Nuitka，请先安装：pip install nuitka"
            exit 1
        fi
        if [ "${2:-}" = "--onefile" ]; then
            "$PYTHON" -m nuitka --follow-imports --standalone --enable-plugin=tk-inter \
                --include-data-dir=assets=assets "${ICON_OPTS[@]}" \
                --onefile \
                --product-version=1.0.2 --product-name="抽学号" --company-name=hanhan_boy choose.py
        else
            "$PYTHON" -m nuitka --follow-imports --standalone --enable-plugin=tk-inter \
                --include-data-dir=assets=assets "${ICON_OPTS[@]}" \
                --product-version=1.0.2 --product-name="抽学号" --company-name=hanhan_boy choose.py
        fi
        ;;
    --pyinstaller)
        # 检查 PyInstaller 是否可用（默认已安装，仅作友好提示）
        if ! command -v pyinstaller >/dev/null 2>&1; then
            echo "错误：未找到 PyInstaller，请先安装：pip install pyinstaller"
            exit 1
        fi
        # PyInstaller 的图标参数为 --icon（各平台通用），重新设置
        ICON_OPTS=()
        if [ -f "$ICON" ]; then
            ICON_OPTS=("--icon=$ICON")
        fi
        # Linux/macOS 的 --add-data 分隔符为 ':'（Windows 为 ';'）
        if [ "${2:-}" = "--onefile" ]; then
            pyinstaller --noconfirm --onefile --windowed "${ICON_OPTS[@]}" \
                --add-data --clean "assets:assets" choose.py
        else
            pyinstaller --noconfirm --windowed "${ICON_OPTS[@]}" \
                --add-data --clean "assets:assets" choose.py
        fi
        ;;
    *)
        echo "Invalid argument. Use --nuitka or --pyinstaller."
        exit 1
        ;;
esac

echo "打包完成。"
