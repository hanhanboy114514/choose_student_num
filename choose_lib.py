# -*- coding: utf-8 -*-

import random

__all__ = ["gl", "bac", "ba", "nomal", "load_from_file", "custom"]

# ============================ 卡池内容 ============================
# 名称与内容与原文件一致，仅将 list 改为 tuple（不可变），防止被误改

# 五星（高稀有度）对应学号
xdwx = (1, 13, 16, 34, 35, 44)
# 四星（陪跑 / 歪池）学号
czwx = (11, 9, 29, 22, 32)
# 常驻五星对应学号
ycwx = (2, 10, 15, 17, 27)
# 联动五星角色名（对应学号 46~49）
xdycwx = ('后藤独', '伊地知虹夏', '山田凉', '喜多郁代')
xdycwx2 = (46, 47, 48, 49)
# 三星学号
sx = (6, 8, 12, 19, 21, 22, 23, 25, 28, 31, 39, 41, 43, 45)
# 二星学号
sanx = (3, 4, 5, 7, 14, 18, 20, 24, 26, 30, 33, 36, 37, 38, 40, 42)
# 蔚蓝档案角色名：三星（修复了原 '鹤城''亚子' 缺少逗号的问题）
s3 = ('一花', '和纱', '夏', '小春', '忧', '日向', '日富美', '未花', '梓', '樱子', '渚', '玲纱', '真白', '美弥',
      '鹤城', '亚子', '伊吕波', '伊织', '惠', '日奈', '晴奈', '泉', '濑名', '爱露', '霞', '千寻', '响', '堇',
      '妮露', '小雪', '日鞠', '时', '柚子', '爱丽丝', '真纪', '绿', '艾米', '花凛', '诺亚', '切里诺', '和香',
      '实梨', '时雨', '巴', '芽瑠', '真里奈', '康娜', '吹雪', '咲', '宫子', '美游', '萌绘', '三森', '月咏', '若藻')
# 蔚蓝档案角色名：二星
s2 = ('爱理', '玛丽', '花江', '莲见', '佳代子', '明里', '风香', '睦月', '纯子', '桃井', '优香', '晴', '茜',
      '红叶', '桐乃', '千世', '椿', '泉奈', '菲娜', '静子', '花子', '芹香')
# 蔚蓝档案角色名：一星
s1 = ('好美', '志美子', '芹娜', '铃美', '伊吹', '千夏', '朱莉', '春香', '小玉', '明日奈', '琴里')


def _append_nine_blue_one_gold(rt1: list, rt2: list, blue_pool: tuple, gold_pool: tuple) -> None:
    """九蓝一金：追加 9 个蓝色 + 1 个金色（抽数计数由调用方另行处理）。"""
    for _ in range(9):
        rt1.append(str(random.choice(blue_pool)))
        rt2.append("blue")
    rt1.append(str(random.choice(gold_pool)))
    rt2.append("yellow")


def _draw_student_numbers(ab: int, high_color: str, sx_color: str,
                          blue_gold_pools=None,checkbuttons2: int = 0) -> tuple:
    """通用“学号抽卡”引擎（gl 与 ba 共用，分支顺序与原版一致）。

    参数:
        ab: 需要抽取的个数
        high_color: 限定五星、常驻五星、联动五星的颜色（gl 为 yellow，ba 为 magenta）
        sx_color: 命中三星学号的颜色（gl 为 magenta，ba 为 yellow）
        fallback_pool: 其余数字的抽取池（ba 传 None 表示不产出）
        blue_gold_pools: (九蓝一金)，仅 ba 的 s==50 分支使用
        checkbuttons2: 是否启用 "mind maneger" 特殊结果
    """
    rt1 = []
    rt2 = []
    while len(rt1) < ab:
        s = random.randint(1, 100)
        if s <= 3:
            p = random.randint(1, 3)
            rt1.append(str(random.choice(xdwx if p == 2 else czwx)))
            rt2.append(high_color)
        elif s > 3 and s <=33:
            rt1.append(str(random.choice(sx)))
            rt2.append(sx_color)
        elif s > 33 and s <= 93:
            rt1.append(str(random.choice(sanx)))
            rt2.append("blue")
        elif s == 94:
            p = random.randint(1, 100)
            rt1.append(str(random.choice(ycwx if p == 1 or p == 2 else czwx)))
            rt2.append(high_color)
        elif s == 95:
            p = random.randint(1, 100)
            rt1.append(str(random.choice(xdycwx if p == 1 else czwx)))
            rt2.append(high_color)
        elif s > 96 and blue_gold_pools is not None:
            # 九蓝一金（仅 ba；gl 的随机数上限为 49，不会命中）
            # 修复：仅当剩余条数足够容纳完整 10 连（9 蓝 + 1 金）时才触发，
            # 否则退化为单抽蓝，保证结果条数恰好等于 ab（原版会超出设定值）
            if len(rt1) + 10 <= ab:
                _append_nine_blue_one_gold(rt1, rt2, blue_gold_pools[0], blue_gold_pools[1])
            else:
                rt1.append(str(random.choice(blue_gold_pools[0])))
                rt2.append("blue")
        elif s == 95:
            if checkbuttons2 == 1:
                rt1.append("mind maneger")
                rt2.append("mind maneger")
            else:
                rt1.append(str(random.choice(sx)))
                rt2.append("yellow")
        else:
            rt1.append(str(random.choice(sanx)))
            rt2.append("blue")
    return rt1, rt2


# ============================ 对外接口 ============================
def gl(ab: int) -> tuple:
    '''原神模式抽学号'''
    return _draw_student_numbers(ab , high_color="yellow",
                                 sx_color="magenta")


def bac(ab: int, checkbuttons2: int) -> tuple:
    '''蔚蓝档案角色抽卡（已修复：结果条数恰好等于 ab，不再超额）'''
    rt1 = []
    rt2 = []
    i = 0
    while i < ab:
        s = random.randint(1, 100)
        if s <= 3:   #3%三星
            p = random.randint(1, 100)
            rt1.append(str(random.choice(s3)))
            rt2.append("magenta")
        elif s > 3 and s <= 33:  #30%三星
            rt1.append(str(random.choice(s2)))
            rt2.append("yellow")
        elif s > 33 and s <= 93:  #60%三星
            rt1.append(str(random.choice(s2)))
            rt2.append("blue")
        elif s == 94:
            # 九蓝一金：仅当剩余条数足够容纳 10 连时才触发
            # （修复原版 ab+1-i>=10 的差一错误导致的超额；此处 i 恒等于 len(rt1)）
            if len(rt1) + 10 <= ab:
                _append_nine_blue_one_gold(rt1, rt2, s1, s2)
                i += 9
            else:
                rt1.append(str(random.choice(s1)))
                rt2.append("blue")
        elif s == 95:
            if checkbuttons2 == 1:
                rt1.append("mind maneger")
                rt2.append("mind maneger")
            else:
                rt1.append(str(random.choice(sx)))
                rt2.append("yellow")
        else:  # s == 100
            i -= 1  # 不产出，继续抽取
        i += 1
    return rt1, rt2


def ba(ab: int, checkbuttons2: int) -> tuple:
    '''蔚蓝档案模式抽学号（已修复：结果条数恰好等于 ab，不再超额）'''
    return _draw_student_numbers(ab, high_color="magenta",
                                 sx_color="yellow",
                                 blue_gold_pools=(sanx, sx),
                                 checkbuttons2=checkbuttons2)


def nomal(ab: int) -> list:
    '''正常模式抽学号'''
    return [str(random.randint(1, 50)) for _ in range(ab)]


def load_from_file(file_path: str, strip: bool = True, skip_empty: bool = True) -> tuple:
    """
    从外部文本文档导入数据为列表，一行一个数据。

    参数:
        file_path: 文本文件的路径（支持绝对路径和相对路径）
        strip: 是否去除每行首尾空白字符，默认为 True
        skip_empty: 是否跳过空行，默认为 True

    返回:
        包含文件各行内容的列表+稀有度列表，若文件不存在或读取失败则返回两个空列表。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            line_gold = []
            line_blue = []
            line_magenta = []
            line_empty = []
            lines = (line.strip() if strip else line.rstrip('\n') for line in f)
            if skip_empty:
                lines = (line for line in lines if line)
            line = list(lines)
            for i in line:
                if "#" in i:
                    _ = i[i.find("#")+1:]
                    _s = i[:i.find("#")]
                    _ = _.strip()
                    _s = _s.strip()
                    if _ == "gold":
                        line_gold.append(_s)
                    elif _ == "blue":
                        line_blue.append(_s)
                    elif _ == "purple":
                        line_magenta.append(_s)
                    else:
                        line_empty.append(_s)
                else:
                    line_empty.append(i)
            return line_gold, line_blue, line_magenta, line_empty
    except FileNotFoundError:
        print(f"错误：找不到文件 '{file_path}'")
        return [], []
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return [], []


def custom(list_high: list, list_sx: list, list_sanx: list, list_empty: list,
           ab: int, high_color = "yellow", sx_color = "magenta") -> tuple:
    '''自定义模式抽学号'''
    rt1 = []
    rt2 = []
    while len(rt1) < ab:
        s = random.randint(1, 100)
        if s <= 3:
            if len(list_high) == 0:
                rt1.append(str(random.choice(list_empty)))
                rt2.append("empty")
            else:
                rt1.append(str(random.choice(list_high)))
                rt2.append(high_color)
        elif s > 3 and s <=33:
            if len(list_sx) == 0:
                rt1.append(str(random.choice(list_empty)))
                rt2.append("empty")
            else:
                rt1.append(str(random.choice(list_sx)))
                rt2.append(sx_color)
        elif s > 33 and s <= 93:
            if len(list_sanx) == 0:
                rt1.append(str(random.choice(list_empty)))
                rt2.append("empty")
            else:
                rt1.append(str(random.choice(list_sanx)))
                rt2.append("blue")
        else:
            if len(list_empty) == 0:
                pass
            else:
                rt1.append(str(random.choice(list_empty)))
                rt2.append("empty")
    return rt1, rt2
