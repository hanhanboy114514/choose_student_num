import tkinter as tk
import choose_lib as choose
from tkinter import messagebox
import sys
import os
from PIL import Image, ImageTk
from tkinter import filedialog
import webbrowser
from pathlib import Path
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
def mind_maneger():
    '''神经资源管理器'''
    def b():
        window.destroy()
    def a():
        second=tk.Toplevel(root_window)
        second.title('神经资源管理器')
        second.geometry("350x170")
        second.iconbitmap(get_resource_path("assets/12.ico"))
        t1ext = tk.Label(second,text="你似了",font=("微软雅黑",30),fg="#0033a7")
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
    window.geometry('350x170')
    window.iconbitmap(get_resource_path("assets/12.ico"))
    text = tk.Label(window,text="  脑子 未响应",font=("微软雅黑", 12),fg='#0033a7')
    text.pack(anchor="w",fill="y",pady=6)
    la2 = tk.Label(window,text="  如果关闭此器官，可能会当场暴毙\n",font=("微软雅黑", 10))
    la2.pack(anchor="w")
    la3 = tk.Button(window,text="  → 关闭器官",font=("微软雅黑",15),fg="#0078d7",bd=0,command=a)
    la3.pack(anchor="w")
    la4 = tk.Button(window,text="  → 等待器官响应",font=("微软雅黑",15),fg="#0078d7",bd=0,command=b)
    la4.pack(anchor="w",fill="y",pady=6)
def mod():
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
                a=choose.load_from_file(file_path)  # type: ignore # Just to check if the file can be opened
        except FileNotFoundError:
            messagebox.showerror("错误", "未找到指定文件", parent=root_window)
            return
        rt1=choose.custom(a,int(e1.get()))
        for i in range(len(rt1)):
            e2.insert(tk.END,rt1[i]+"\n","white")
def Ciallo():
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
    ciallo.geometry("400x100")
    center_window(ciallo, 400, 100)
    ciallo.iconbitmap(get_resource_path("assets/7.ico"))
    ciallo.resizable(False,False)
    t1=tk.Entry(ciallo,width=56)
    t1.grid(row=0)
    b2=tk.Button(ciallo,text="确定",font=("微软雅黑",12),command=Homo)
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
    img = img.resize((240,150))
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
    center_window(h114514, 240, 150)
    h114514.iconbitmap(get_resource_path("assets/7.ico"))
    h114514.resizable(False,False)
    t1 = tk.Label(h114514,image=photo)
    t1.image = photo # type: ignore
    t1.pack()
def center_window(root, width, height):
    # 获取屏幕尺寸
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()

    # 计算窗口居中显示的参数
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)

    # 设置窗口居中显示
    root.geometry(size)
# 调用Tk()创建主窗口
root_window =tk.Tk()
checkbuttons1=tk.IntVar()
checkbuttons1.set(1)
checkbuttons2=tk.IntVar()
checkbuttons3=tk.IntVar()
checkbuttons3.set(1)
v=tk.IntVar()
v.set(4)
# 给主窗口起一个名字，也就是窗口的名字
root_window.title('抽学号')
center_window(root_window, 750, 650)
root_window.iconbitmap(get_resource_path("assets/bg_cs_r_00.ico"))
root_window.resizable(False, False)
# 菜单栏
menu_bar = tk.Menu(root_window)
root_window.config(menu=menu_bar)
file_menu=tk.Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label="帮助",menu=file_menu)
file_menu.add_command(label="彩蛋",command=Ciallo)
file_menu.add_command(label="关于",command=lambda: messagebox.showinfo("关于","2026©hanhan_boy Version 1.0.1",parent=root_window))
# 主界面
text = tk.Label(root_window,bg="#F5F5F7",text="欢迎来到抽学号程序！\n此程序目前有两个模式：\nBlue Archieve(BA)模式和Genshin Impact（GI）模式\nBA有概率触发九蓝一金，GI模式没有\n有概率抽卡次数没达到设定的值\nBA有概率弹出“脑子 未响应”弹窗，如果选择关闭器官选项，则会直接关闭程序，不管后面选了其他选项\n为保障您的使用体验，这边建议选择GI模式。",font=("微软雅黑", 12))
text.grid(row=0,column=0,columnspan=4)
r1=tk.Radiobutton(root_window,bg="#F5F5F7",text="BA模式",variable=v,value=1)
r1.grid(row=1,column=0)
r2=tk.Radiobutton(root_window,bg="#F5F5F7",text="GI模式",variable=v,value=2)
r2.grid(row=2,column=0)
r3=tk.Radiobutton(root_window,bg="#F5F5F7",text="BA角色模式",variable=v,value=3)
r3.grid(row=3,column=0)
r4=tk.Radiobutton(root_window,bg="#F5F5F7",text="正常模式",variable=v,value=4)
r4.grid(row=4,column=0)
r5=tk.Radiobutton(root_window,bg="#F5F5F7",text="自定义模式",variable=v,value=5)
r5.grid(row=5,column=0)
l1=tk.Label(root_window,bg="#F5F5F7",text="次数",font=("微软雅黑", 12)).grid(row=1,column=1)
c1=tk.Checkbutton(root_window,bg="#F5F5F7",text="进行下一次抽时是否清空文本框",variable=checkbuttons1)
c1.grid(row=2,column=1)
c2=tk.Checkbutton(root_window,bg="#F5F5F7",text="是否弹出“神经资源管理器”",variable=checkbuttons2)
c2.grid(row=3,column=1)
c3=tk.Checkbutton(root_window,bg="#F5F5F7",text="自定义模式是否使用上一次的设置",variable=checkbuttons3)
c3.grid(row=4,column=1)
e1=tk.Entry(root_window,bd=2)
e1.grid(row=1,column=2,columnspan=2)
b1=tk.Button(root_window,bg="#F5F5F7",text="抽学号",font=("微软雅黑", 12),command=mod)
b1.grid(row=2,column=2)
e2=tk.Text(root_window,width=80)
e2.grid(row=6,column=0,columnspan=4)
scrollbar = tk.Scrollbar(root_window, orient='vertical', command=e2.yview)
scrollbar.grid(row=6,column=3,sticky='ns')
e2.config(bg="grey",font=("微软雅黑", 12),yscrollcommand=scrollbar.set,width=70,height=14)
e2.tag_configure("blue",foreground="blue")
e2.tag_configure("white",foreground="white")
e2.tag_configure("yellow",foreground="yellow")
e2.tag_configure("magenta",foreground="magenta")
root_window.configure(bg="#F5F5F7")
root_window.bind('<Return>', lambda event: mod())
root_window.bind('<KP_Enter>', lambda event: mod())
root_window.mainloop()