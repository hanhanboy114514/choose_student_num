import tkinter as tk
import tkinter.font as tkfont
import choose_lib as choose
from tkinter import messagebox
import sys
import os
from PIL import Image, ImageTk
from tkinter import filedialog
import webbrowser 
from pathlib import Path
import ctypes
def get_resource_path(relative_path: str) -> Path:
    """统一获取资源绝对路径（只读场景）"""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # PyInstaller 兼容分支（留作扩展）
        base_path = Path(sys._MEIPASS) # type: ignore
    elif getattr(sys, 'frozen', False):
        # Nuitka --onefile：使用 sys.executable 所在目录的临时资源根
        # Nuitka 1.5+ 提供了 nuitka.__compiled__ 和 nuitka.utils.execution.getTempDir()
        try:
            from nuitka.utils.execution import getTempDir # type: ignore
            temp_root = Path(getTempDir())
            # 查找以 .nuitka- 开头的最近子目录（匹配实际解压结构）
            candidates = list(temp_root.glob(".nuitka-*"))
            if candidates:
                base_path = candidates[0]
            else:
                base_path = temp_root
        except (ImportError, OSError):
            # 回退：尝试从 sys.executable 推导（适用于 onedir 或部分 onefile）
            base_path = Path(sys.executable).parent
    else:
        # 未冻结：开发态，直接基于当前模块位置
        base_path = Path(__file__).parent
    
    return (base_path / relative_path).resolve()
def set_window_icon(window, icon_path: str) -> None:
    """跨平台设置窗口图标。

    Windows 的 Tk 支持 iconbitmap(.ico)；Linux/macOS 的 Tk 无法解析 .ico 位图
    （运行时会报 TclError: bitmap ... not defined），因此改用 PIL 读取图标后
    通过 iconphoto 设置。任何失败都静默跳过，避免无图标环境下程序崩溃。
    """
    try:
        if sys.platform == "win32":
            window.iconbitmap(icon_path)
        else:
            img = ImageTk.PhotoImage(Image.open(icon_path).convert("RGBA"))
            window.iconphoto(True, img)
            window._icon_ref = img  # 保持引用，防止被垃圾回收后图标消失
    except Exception:
        pass
def mind_maneger():
    '''神经资源管理器'''
    def b():
        window.destroy()
    def a():
        second=tk.Toplevel(root_window)
        second.title('神经资源管理器')
        w2,h2=scaled_size(350,170)
        center_window(second,w2,h2)
        set_window_icon(second, get_resource_path("assets/12.ico")) # type: ignore
        t1ext = tk.Label(second,text="你似了",font=("微软雅黑",font_scale(30)),fg="#0033a7")
        t1ext.pack(anchor="w")
        second.mainloop()
        sys.exit(0)
    global window
    # 调用Tk()创建主窗口
    window =tk.Toplevel(root_window)
    # 给主窗口起一个名字，也就是窗口的名字
    window.title('神经资源管理器')
    window.resizable(False, False)
    # 设置焦点
    window.focus_set()
    
    # 设置模态（新窗口关闭前无法操作主窗口）
    window.grab_set()
    
    # 当窗口关闭时释放grab
    window.protocol("WM_DELETE_WINDOW", lambda: on_close(window))

    def on_close(window):
        window.grab_release()
        window.destroy()
    ww,wh=scaled_size(350,170)
    center_window(window,ww,wh)
    set_window_icon(window, get_resource_path("assets/12.ico")) # type: ignore
    text = tk.Label(window,text="  脑子 未响应",font=("微软雅黑", font_scale(12)),fg='#0033a7')
    text.pack(anchor="w",fill="y",pady=6)
    la2 = tk.Label(window,text="  如果关闭此器官，可能会当场暴毙\n",font=("微软雅黑", font_scale(10)))
    la2.pack(anchor="w")
    la3 = tk.Button(window,text="  → 关闭器官",font=("微软雅黑",font_scale(15)),fg="#0078d7",bd=0,command=a)
    la3.pack(anchor="w")
    la4 = tk.Button(window,text="  → 等待器官响应",font=("微软雅黑",font_scale(15)),fg="#0078d7",bd=0,command=b)
    la4.pack(anchor="w",fill="y",pady=6)
def mod():
    """
    判断当前选择的模式，并调用相应的抽学号函数。
    """
    global data
    data=""
    if checkbuttons1.get() == 1:
        e2.delete(0.0,tk.END)
    if v.get()==1:
        #蔚蓝档案模式抽学号
        rt1,rt2=choose.ba(int(e1.get()),checkbuttons2.get())
        for i in range(len(rt1)):
            if checkbuttons2.get() == 1 and rt1[i] == "mind maneger":
                mind_maneger()
                window.wait_window()
            else:
                e2.insert(tk.END,rt1[i]+"\n",rt2[i])
    elif v.get()==2:
        #原神模式抽学号
        rt1,rt2=choose.gl(int(e1.get()))
        for i in range(len(rt1)):
            if checkbuttons2.get() == 1 and rt1[i] == "mind maneger":
                mind_maneger()
                window.wait_window()
            else:
                e2.insert(tk.END,rt1[i]+"\n",rt2[i])
    elif v.get()==3:
        #蔚蓝档案角色模式抽学号
        rt1,rt2=choose.bac(int(e1.get()),checkbuttons2.get())
        for i in range(len(rt1)):
            if checkbuttons2.get() == 1 and rt1[i] == "mind maneger":
                mind_maneger()
                window.wait_window()
            else:
                e2.insert(tk.END,rt1[i]+"\n",rt2[i])
    elif v.get()==4:
        #正常模式抽学号
        rt1=choose.nomal(int(e1.get()))
        for i in range(len(rt1)):
            e2.insert(tk.END,rt1[i]+"\n","white")
    elif v.get()==5:
        #自定义模式抽学号
        if os.path.exists("tmp/tmp.txt") == False or checkbuttons3.get() == 0:
            result = messagebox.askquestion("提示","请选择一个文本文件，文件内每行一个学号",parent=root_window)
            if result == 'yes':
                file_path = filedialog.askopenfilename(title="选择学号文件", filetypes=[("文本文件", "*.txt")])
                os.makedirs("tmp", exist_ok=True)
                with open("tmp/tmp.txt", 'w') as f:
                    f.write(file_path)
        else:
            with open("tmp/tmp.txt", 'r') as f:
                file_path = f.read()
        try:
            with open(file_path, 'r') as f: # type: ignore
                line_gold, line_blue, line_magenta, line_empty=choose.load_from_file(file_path)  # type: ignore # Just to check if the file can be opened
        except FileNotFoundError:
            messagebox.showerror("错误", "未找到指定文件", parent=root_window)
            return
        rt1,rt2=choose.custom(line_gold, line_blue, line_magenta,line_empty, int(e1.get()))
        for i in range(len(rt1)):
            if rt2[i] == "empty":
                _ = "white"
            else:
                _ = rt2[i]
            e2.insert(tk.END,rt1[i]+"\n", _ )
def Ciallo():
    """
    彩蛋窗口
    """
    def Homo():
        homoin=t1.get()
        if homoin == "homo" or homoin == "114514" or homoin == "1919810" or homoin == "homo114514" or homoin == "homo1145141919810":
            homo114514()
        elif homoin == "0721" or homoin == "ciallo" or homoin == "yuzusoft":
            c0721()
        else:
            messagebox.showinfo("信息","Ciallo～(∠・ω< )⌒★",parent=ciallo)
    ciallo=tk.Toplevel(root_window)
    # 设置焦点
    ciallo.focus_set()
    
    # 设置模态（新窗口关闭前无法操作主窗口）
    ciallo.grab_set()
    
    # 当窗口关闭时释放grab
    ciallo.protocol("WM_DELETE_WINDOW", lambda: on_close(ciallo))

    def on_close(window):
        window.grab_release()
        window.destroy()
    ciallo.title("彩蛋")
    cw,ch=scaled_size(400,100)
    center_window(ciallo, cw, ch)
    set_window_icon(ciallo, get_resource_path("assets/favicon.ico")) # type: ignore
    ciallo.resizable(False,False)
    t1=tk.Entry(ciallo,width=56)
    t1.grid(row=0)
    b2=tk.Button(ciallo,text="确定",font=("微软雅黑",font_scale(12)),command=Homo)
    b2.grid(row=1)
    # 绑定回车键到按钮
    ciallo.bind('<Return>', lambda event: Homo())
    # 如果需要数字键盘的回车键也有效
    ciallo.bind('<KP_Enter>', lambda event: Homo())
    def c0721():
        URL="https://www.bilibili.com/video/BV1L4421S7Kr"
        webbrowser.open(URL)
    def homo114514():
        img = Image.open(get_resource_path('assets/1234.png'))
        iw,ih=scaled_size(240,150)
        img = img.resize((iw,ih))
        photo = ImageTk.PhotoImage(img)
        h114514 = tk.Toplevel(root_window)
        # 设置焦点
        h114514.focus_set()
        
        # 设置模态（新窗口关闭前无法操作主窗口）
        h114514.grab_set()
        
        # 当窗口关闭时释放grab
        h114514.protocol("WM_DELETE_WINDOW", lambda: on_close(h114514))

        def on_close(window):
            window.grab_release()
            window.destroy()
        h114514.title("homo")
        hw,hh=scaled_size(240,150)
        center_window(h114514, hw, hh)
        set_window_icon(h114514, get_resource_path("assets/7.ico")) # type: ignore
        h114514.resizable(False,False)
        t1 = tk.Label(h114514,image=photo)
        t1.image = photo # type: ignore
        t1.pack()
# ============ 不同分辨率 / 高分屏 适配 ============
# 主窗口的设计尺寸（其它窗口按同一套比例缩放）。
# 原来的设计 1320x1100 在高分屏上几乎占满全屏，现改为原来的一半（660x550）；
# 主窗口允许拖动调整大小，窗口内的结果区会随窗口大小自适应伸缩。
MAIN_WINDOW_W = 750
MAIN_WINDOW_H = 650
# 窗口边缘距离屏幕边缘保留的空隙（逻辑像素）
FIT_MARGIN = 30
# 屏幕 DPI 缩放系数（100% = 1.0）与界面缩放系数（越小代表屏幕越“放不下”）
DPI_SCALE = 1.0
UI_SCALE = 1.0


def enable_dpi_awareness() -> None:
    """在创建任何 Tk 窗口前启用 Windows 进程级 DPI 感知。

    不感知时 Windows 会把屏幕分辨率“虚拟化”，若再手动放大字体就会出现
    双重缩放、窗口坐标错位。非 Windows 平台直接跳过；若程序已通过清单等
    方式启用过则忽略失败，只需确认实际生效即可。
    """
    global DPI_ENABLED
    if sys.platform != "win32":
        DPI_ENABLED = False
        return
    DPI_ENABLED = False
    try:
        if ctypes.windll.shcore.SetProcessDpiAwareness(1) == 0:  # PROCESS_SYSTEM_DPI_AWARE
            DPI_ENABLED = True
            return
    except Exception:
        pass
    try:
        # 已经启用（例如编译产物自带 DPI 清单）时查询实际状态
        aware = ctypes.c_int(0)
        ctypes.windll.shcore.GetProcessDpiAwareness(None, ctypes.byref(aware))
        DPI_ENABLED = aware.value > 0
    except Exception:
        try:
            DPI_ENABLED = bool(ctypes.windll.user32.SetProcessDPIAware())
        except Exception:
            DPI_ENABLED = False


def compute_dpi_scale(root) -> float:
    """根据当前系统的 DPI 缩放比例计算 DPI_SCALE（100% 缩放时为 1.0）。"""
    global DPI_SCALE
    if not DPI_ENABLED:
        DPI_SCALE = 1.0  # 未启用感知：坐标天然就是“逻辑像素”，交给系统放大
        return DPI_SCALE
    try:
        if sys.platform == "win32":
            scale = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100.0
            if scale > 0:
                DPI_SCALE = scale
                return DPI_SCALE
    except Exception:
        pass
    try:
        # 回退：用 Tk 实测的每英寸像素数推算（96 dpi = 100%）
        DPI_SCALE = max(1.0, root.winfo_fpixels('1i') / 96.0)
    except Exception:
        DPI_SCALE = 1.0
    return DPI_SCALE


def setup_tk_scaling(root) -> None:
    """Windows 高分屏下让 Tk 的字号（点）正确换算成物理像素。

    启用 DPI 感知后必须把 tk scaling 调成 dpi/72，否则字号会偏小；
    其它平台沿用 Tk 默认值，避免改变原有观感。
    """
    if sys.platform != "win32":
        return
    try:
        # 96 dpi 时每点像素为 96/72≈1.333，乘以 DPI_SCALE 即可
        root.tk.call('tk', 'scaling', (96.0 / 72.0) * DPI_SCALE)
    except Exception:
        pass


def compute_ui_scale(root) -> float:
    """按当前屏幕分辨率计算界面缩放比例（只缩小、不放大）。

    以主窗口设计尺寸为基准：屏幕比设计尺寸小多少，就把窗口和字号缩小多少，
    保证程序在任何分辨率下都能完整显示。
    """
    global UI_SCALE
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    # 换算成逻辑分辨率后再判断，避免高分屏缩放干扰
    logical_w = screen_w / DPI_SCALE
    logical_h = screen_h / DPI_SCALE
    avail_w = max(logical_w - 2 * FIT_MARGIN, 1)
    avail_h = max(logical_h - 2 * FIT_MARGIN, 1)
    UI_SCALE = max(0.6, min(1.0, avail_w / MAIN_WINDOW_W, avail_h / MAIN_WINDOW_H))
    return UI_SCALE


def font_scale(points) -> int:
    """把设计稿字号换算为适配当前屏幕的字号（返回点数）。"""
    return max(1, round(points * UI_SCALE))


def scale_default_fonts(root) -> None:
    """按 UI_SCALE 缩放 Tk 内置的默认字体。

    没有显式指定字体的控件（单选框、输入框、菜单等）用的是 Tk 默认字体，
    不缩放的话在小屏上会显得比别的控件大，甚至把窗口撑破。
    """
    try:
        for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont",
                     "TkCaptionFont", "TkSmallCaptionFont", "TkIconFont", "TkTooltipFont"):
            font = tkfont.nametofont(name)
            size = font.cget("size")
            if isinstance(size, int) and size > 0:
                font.configure(size=max(1, round(size * UI_SCALE)))
    except Exception:
        pass


def scaled_size(width, height):
    """把设计稿的像素尺寸换算为实际屏幕像素（含 DPI 缩放）。"""
    return (max(1, round(width * UI_SCALE * DPI_SCALE)),
            max(1, round(height * UI_SCALE * DPI_SCALE)))


def px_len(logical_px) -> int:
    """把“逻辑像素”换算成当前 DPI 下的物理像素（用于间距、边距等像素属性）。"""
    return max(1, round(logical_px * UI_SCALE * DPI_SCALE))


def unit_scale(chars) -> int:
    """把字符/行数等“文本单位”按 UI_SCALE 缩放。

    文本单位自身会随 tk scaling 和字号自动换算，因此只按分辨率缩小、
    不需要再乘 DPI_SCALE。
    """
    return max(1, round(chars * UI_SCALE))


def center_window(root, width, height):
    """把窗口居中显示。

    - 坐标一律取整，避免出现半个像素导致窗口“看起来没居中”；
    - 窗口比可用屏幕大时先等比收缩，保证整体可见；
    - 坐标下限为 0，防止任务栏/多屏布局下被顶出屏幕。
    """
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    fit_w = max(screenwidth - 2 * FIT_MARGIN * DPI_SCALE, 1)
    fit_h = max(screenheight - 2 * FIT_MARGIN * DPI_SCALE, 1)
    fit = max(0.6, min(1.0, fit_w / width, fit_h / height))
    w = max(1, round(width * fit))
    h = max(1, round(height * fit))
    x = max(0, (screenwidth - w) // 2)
    y = max(0, (screenheight - h) // 2)
    # 设置窗口居中显示
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


# 必须先开启 DPI 感知、再创建窗口，窗口才会用真实的物理像素定位
enable_dpi_awareness()
# 调用Tk()创建主窗口
root_window =tk.Tk()
compute_dpi_scale(root_window)
setup_tk_scaling(root_window)
compute_ui_scale(root_window)
scale_default_fonts(root_window)
# 设置相关变量
checkbuttons1=tk.IntVar()
checkbuttons1.set(1)
checkbuttons2=tk.IntVar()
checkbuttons3=tk.IntVar()
checkbuttons3.set(1)
v=tk.IntVar()
v.set(4)
# 初始化窗口
root_window.title('抽学号')
main_w, main_h = scaled_size(MAIN_WINDOW_W, MAIN_WINDOW_H)
center_window(root_window, main_w, main_h)
set_window_icon(root_window, get_resource_path("assets/favicon.ico")) # type: ignore
root_window.resizable(True, True)  # 允许拖动调整窗口大小，内容随窗口自适应
# 菜单栏
menu_bar = tk.Menu(root_window)
root_window.config(menu=menu_bar)
file_menu=tk.Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label="帮助",menu=file_menu)
file_menu.add_command(label="彩蛋",command=Ciallo)
file_menu.add_command(label="关于",command=lambda: messagebox.showinfo("关于","2026©hanhan_boy Version 1.0.2",parent=root_window))
# ============ 主界面（内容随窗口大小自适应） ============
# 顶部说明文字：字号更小，宽度随窗口自动换行
text = tk.Label(root_window,bg="#F5F5F7",justify="left",text="""欢迎来到抽学号程序！
此程序目前有两个模式：
Blue Archieve(BA)模式和Genshin Impact（GI）模式
BA有概率弹出“脑子 未响应”弹窗，如果选择关闭器官选项，则会直接关闭程序
为保障您的使用体验，这边建议选择GI模式。""",font=("微软雅黑", font_scale(10)))
text.grid(row=0,column=0,columnspan=4,sticky="ew",padx=px_len(10),pady=px_len(6))

def fit_intro(_event=None):
    """让顶部说明文字随窗口宽度自动换行，避免被截断。"""
    try:
        w = root_window.winfo_width()
        if w > px_len(60):
            text.configure(wraplength=max(px_len(60), w - px_len(30)))
    except Exception:
        pass

root_window.bind('<Configure>', fit_intro)
fit_intro()

r1=tk.Radiobutton(root_window,bg="#F5F5F7",text="BA模式",variable=v,value=1)
r1.grid(row=1,column=0,sticky="w",padx=px_len(8))
r2=tk.Radiobutton(root_window,bg="#F5F5F7",text="GI模式",variable=v,value=2)
r2.grid(row=2,column=0,sticky="w",padx=px_len(8))
r3=tk.Radiobutton(root_window,bg="#F5F5F7",text="BA角色模式",variable=v,value=3)
r3.grid(row=3,column=0,sticky="w",padx=px_len(8))
r4=tk.Radiobutton(root_window,bg="#F5F5F7",text="正常模式",variable=v,value=4)
r4.grid(row=4,column=0,sticky="w",padx=px_len(8))
r5=tk.Radiobutton(root_window,bg="#F5F5F7",text="自定义模式",variable=v,value=5)
r5.grid(row=5,column=0,sticky="w",padx=px_len(8))
l1=tk.Label(root_window,bg="#F5F5F7",text="次数",font=("微软雅黑", font_scale(10)))
l1.grid(row=1,column=1,sticky="w",padx=px_len(6))
c1=tk.Checkbutton(root_window,bg="#F5F5F7",text="进行下一次抽时是否清空文本框",variable=checkbuttons1)
c1.grid(row=2,column=1,sticky="w",padx=px_len(6))
c2=tk.Checkbutton(root_window,bg="#F5F5F7",text="是否弹出“神经资源管理器”",variable=checkbuttons2)
c2.grid(row=3,column=1,sticky="w",padx=px_len(6))
c3=tk.Checkbutton(root_window,bg="#F5F5F7",text="自定义模式是否使用上一次的设置",variable=checkbuttons3)
c3.grid(row=4,column=1,sticky="w",padx=px_len(6))
e1=tk.Entry(root_window,bd=2)
e1.grid(row=1,column=2,sticky="w",padx=px_len(6))
b1=tk.Button(root_window,bg="#F5F5F7",text="抽学号",font=("微软雅黑", font_scale(10)),command=mod)
b1.grid(row=2,column=2,sticky="w",padx=px_len(6))
# 结果展示区：随窗口大小自动伸缩（拉大窗口时文本区跟着变大）
e2=tk.Text(root_window,bg="grey",font=("微软雅黑", font_scale(10)),width=unit_scale(44),height=unit_scale(10))
e2.grid(row=6,column=0,columnspan=4,sticky="nsew",padx=(px_len(10),px_len(4)),pady=px_len(6))
scrollbar = tk.Scrollbar(root_window, orient='vertical', command=e2.yview)
scrollbar.grid(row=6,column=4,sticky='ns',pady=px_len(6))
e2.config(yscrollcommand=scrollbar.set)
e2.tag_configure("blue",foreground="blue")
e2.tag_configure("white",foreground="white")
e2.tag_configure("yellow",foreground="yellow")
e2.tag_configure("magenta",foreground="magenta")
# 行/列权重：控件所在列保持自然宽度、紧凑排布在左侧；
# 最后一列（第 3 列）和最后一行（第 6 行）吸收窗口伸缩带来的多余空间，
# 让结果文本框随窗口变大而变大、随窗口变小而变小
for col in range(3):
    root_window.grid_columnconfigure(col, weight=0)
root_window.grid_columnconfigure(3, weight=1)
root_window.grid_columnconfigure(4, weight=0, minsize=unit_scale(14))
for row in range(6):
    root_window.grid_rowconfigure(row, weight=0)
root_window.grid_rowconfigure(6, weight=1)
root_window.configure(bg="#F5F5F7")
# 窗口可调整大小：设定最小尺寸，防止把控件挤没
root_window.minsize(px_len(520), px_len(400))
root_window.bind('<Return>', lambda event: mod())
root_window.bind('<KP_Enter>', lambda event: mod())
if str(sys.argv[1:]) == "['test_time']":
    #测量启动用时
    sys.exit(0)
root_window.mainloop()
