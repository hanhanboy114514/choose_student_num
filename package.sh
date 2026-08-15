#!/bin/bash

# 清理旧构建目录
rm -rf dist build choose.build choose.dist choose.onefile-build
rm -f choose.spec

# 判断第一个参数
if [ "$1" = "--nuitka" ]; then
    if [ "$2" = "--onefile" ]; then
        python -m nuitka --follow-imports --standalone --enable-plugin=tk-inter --include-data-dir=assets=assets --windows-icon-from-ico=./assets/bg_cs_r_00.ico --show-progress --windows-console-mod=disable choose.py
    else
        python -m nuitka --follow-imports --standalone --enable-plugin=tk-inter --include-data-dir=assets=assets --windows-icon-from-ico=./assets/bg_cs_r_00.ico --show-progress choose.py
    fi
elif [ "$1" = "--pyinstaller" ]; then
    if [ "$2" = "--onefile" ]; then
        pyinstaller --noconfirm --onefile --windowed --icon=./assets/bg_cs_r_00.ico --add-data "assets:assets" choose.py
    else
        pyinstaller --noconfirm --windowed --icon=./assets/bg_cs_r_00.ico --add-data "assets:assets" choose.py
    fi
else
    echo "Invalid argument. Use --nuitka or --pyinstaller."
    exit 1
fi