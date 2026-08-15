# 抽学号程序
只是一个学生乱写的程序，具体说明在程序本体   
有彩蛋

## 安装
### 一、直接下载
Windows在Github Realess直接下载
### 二、自行编译
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
    pip install ccache #可选，建议安装
    pip install zstandard #可选，压缩单文件
    .\package.bat --nuitka #多文件，生成在choose.dist
    .\package.bat --nuitka --onefile #单文件，直接生成在根目录
使用pyinstaller

    pip install pyinstaller
    .\package.bat --pyinstaller #多文件，生成在dist
    .\package.bat --pyinstaller --onefile #单文件，生成在dist
#### （2）Linux\MacOS
使用nuitka

    pip install nuitka
    pip install ccache #可选，建议安装
    pip install zstandard #可选，压缩单文件
    chmod +x package.sh
    ./package.sh --nuitka #多文件，生成在choose.dist
    ./package.sh --nuitka --onefile #单文件，直接生成在根目录
使用pyinstaller

    pip install pyinstaller
    chmod +x package.sh
    ./package.sh --pyinstaller #多文件，生成在dist
    ./package.sh --pyinstaller --onefile #单文件，生成在dist
如报错"FATAL: tk-inter: Error, it seems 'tk-inter' is not installed."

    sudo apt install python3-tk #包管理软件以实际情况为准
如生成文件后无法运行，命令行显示ModuleNotFoundError: No module named 'PIL'

    pip install pillow