import tkinter as tk
import random
import sys
import os
#定义卡池内容
xdwx=[1,13,16,34,35,44]
czwx=[11,9,29,22,32]
ycwx=[2,10,15,17,27]
xdycwx=['后藤独','伊地知虹夏','山田凉','喜多郁代']
xdycwx2=[46,47,48,49]
sx=[6,8,12,19,21,22,23,25,28,31,39,41,43,45]
sanx=[3,4,5,7,14,18,20,24,26,30,33,36,37,38,40,42]
s3=['一花','和纱','夏','小春','忧','日向','日富美','未花','梓','樱子','渚','玲纱','真白','美弥','鹤城''亚子','伊吕波','伊织','惠','日奈','晴奈','泉','濑名','爱露','霞','千寻','响','堇','妮露','小雪','日鞠','时','柚子','爱丽丝','真纪','绿','艾米','花凛','诺亚','切里诺','和香','实梨','时雨','巴','芽瑠','真里奈','康娜','吹雪','咲','宫子','美游','萌绘','三森','月咏','若藻',]
s2=['爱理','玛丽','花江','莲见','佳代子','明里','风香','睦月','纯子','桃井','优香','晴','茜','红叶','桐乃','千世','椿','泉奈','菲娜','静子','花子',"芹香"]
s1=['好美','志美子','芹娜','铃美','伊吹','千夏','朱莉','春香','小玉','明日奈','琴里']
def gl(ab:int):
    '''原神模式抽学号'''
    rt1=[]
    rt2=[]
    #抽卡主要函数
    while len(rt1) < ab:
        s=random.randint(1,49)
        if s in xdwx:
            p=random.randint(1,9)
            if p%2==0:
                rt1.append(str(random.choice(xdwx)))
                rt2.append("yellow")
            else:
                rt1.append(str(random.choice(czwx)))
                rt2.append("yellow")
        elif s in sx:
            rt1.append(str(s))
            rt2.append("magenta")
        elif s in sanx:
            rt1.append(str(s))
            rt2.append("blue")
        elif s in ycwx:
            p=random.randint(1,10)
            if p%3==0:
                rt1.append(str(random.choice(ycwx)))
                rt2.append("yellow")
            else:
                rt1.append(str(random.choice(czwx)))
                rt2.append("yellow")
        elif s in xdycwx2:
            p=random.randint(1,10)
            if p%3==0:
                rt1.append(str(random.choice(xdycwx)))
                rt2.append("yellow")
            else:
                rt1.append(str(random.choice(czwx)))
                rt2.append("yellow")
        else:
            rt1.append(str(random.choice(sanx)))
            rt2.append("blue")
    return rt1, rt2
def bac(ab:int,checkbuttons2:int):
    '''蔚蓝档案角色抽卡'''
    rt1=[]
    rt2=[]
    i=0
    #抽卡主要函数
    while i<ab:
        s=random.randint(1,51)
        if s <10:
            p=random.randint(1,9)
            if p%2==0:
                rt1.append(str(random.choice(s3)))
                rt2.append("magenta")
            else:
                rt1.append(str(random.choice(s2)))
                rt2.append("magenta")
        elif 10<=s<25:
            rt1.append(str(random.choice(s2)))
            rt2.append("yellow")
        elif 49>=s>=25:
            rt1.append(str(random.choice(s2)))
            rt2.append("blue")
        elif s==50:
            if ab>=10 and ab+1-i>=10:
                for _ in range(9):
                    # 九蓝一金(doge
                    rt1.append(str(random.choice(s1)))
                    rt2.append("blue")
                rt1.append(str(random.choice(s2)))
                rt2.append("yellow")
                i=i+9
            else:
                rt1.append(str(random.choice(s1)))
                rt2.append("blue")
        else:
            if checkbuttons2 == 1:
                rt1.append("mind maneger")
                rt2.append("mind maneger")
            else:
                rt1.append(str(random.choice(s2)))
                rt2.append("yellow")
        i+=1
    return rt1, rt2
def ba(ab:int,checkbuttons2:int):
    '''蔚蓝档案模式抽学号'''  
    rt1=[]
    rt2=[]
    i=0
    #抽卡主要函数
    while len(rt1) < ab:
        s=random.randint(1,51)
        if s in xdwx:
            p=random.randint(1,9)
            if p%2==0:
                rt1.append(str(random.choice(xdwx)))
                rt2.append("magenta")
            else:
                rt1.append(str(random.choice(czwx)))
                rt2.append("magenta")
        elif s in sx:
            rt1.append(str(s))
            rt2.append("yellow")
        elif s in sanx:
            rt1.append(str(s))
            rt2.append("blue")
        elif s in ycwx:
            p=random.randint(1,10)
            if p%3==0:
                rt1.append(str(random.choice(ycwx)))
                rt2.append("magenta")
            else:
                rt1.append(str(random.choice(czwx)))
                rt2.append("magenta")
        elif s in xdycwx2:
            p=random.randint(1,10)
            if p%3==0:
                rt1.append(str(random.choice(xdycwx)))
                rt2.append("magenta")
            else:
                rt1.append(str(random.choice(czwx)))
                rt2.append("magenta")
        elif s==50:
            # 九蓝一金(doge
            if ab>=10 and ab+1-i>=10:
                for _ in range(9):
                    rt1.append(str(random.choice(sanx)))
                    rt2.append("blue")
                rt1.append(str(random.choice(sx)))
                rt2.append("yellow")
            else:
                rt1.append(str(random.choice(sanx)))
                rt2.append("blue")
        elif s==51:
            if checkbuttons2 == 1:
                rt1.append("mind maneger")
                rt2.append("mind maneger")
            else:
                rt1.append(str(random.choice(sx)))
                rt2.append("yellow")
    return rt1, rt2
def nomal(ab:int):
    '''正常模式抽学号'''
    rt1=[]
    #抽卡主要函数
    while len(rt1) < ab:
        rt1.append(str(random.randint(1,50)))
    return rt1

def load_from_file(file_path: str, strip: bool = True, skip_empty: bool = True) -> list:
    """
    从外部文本文档导入数据为列表，一行一个数据。

    参数:
        file_path: 文本文件的路径（支持绝对路径和相对路径）
        strip: 是否去除每行首尾空白字符，默认为 True
        skip_empty: 是否跳过空行，默认为 True

    返回:
        包含文件各行内容的列表

    示例:
        >>> data = load_from_file("students.txt")
        >>> print(data)
        ['张三', '李四', '王五']
    """
    result = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # 处理行内容
                item = line.strip() if strip else line.rstrip('\n')
                # 跳过空行
                if skip_empty and not item:
                    continue
                result.append(item)
        return result
    except FileNotFoundError:
        print(f"错误：找不到文件 '{file_path}'")
        return []
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return []
def custom(a:list,ab:int):
    '''自定义模式抽学号'''
    rt1=[]
    while len(rt1) < ab:
        rt1.append(str(random.choice(a)))
    return rt1