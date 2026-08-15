# 抽学号程序
只是一个学生乱写的程序，具体说明在程序本体   
有彩蛋

## 安装
### 一、直接下载
Windows在Github Realess直接下载
### 二、编译
### 1.克隆
    git clone https://github.com/hanhanboy114514/choose_student_num.git
    cd choose_student_num
### 2.创建虚拟环境
Windows

    py -3 -m venv venv
    .\venv\Scripts\activate
Linux/MacOS

    python3 -m venv venv
    source venv/bin/activate
### 3.编译
#### （1）Windows
使用nuitka

    pip install nuitka
    .\package.bat --nuitka #多文件
    .\package.bat --nuitka --onefile #单文件
使用pyinstaller

    pip install pyinstaller
    .\package.bat --pyinstaller #多文件
    .\package.bat --pyinstaller --onefile #单文件
#### （2）Linux\MacOS
使用nuitka

    pip install nuitka
    chmod +x package.sh
    .\package.sh --nuitka #多文件
    .\package.sh --nuitka --onefile #单文件
使用pyinstaller

    pip install pyinstaller
    chmod +x package.sh
    .\package.sh --pyinstaller #多文件
    .\package.sh --pyinstaller --onefile #单文件