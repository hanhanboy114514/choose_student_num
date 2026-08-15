# -*- coding: utf-8 -*-
"""
choose_lib_optimized.py —— choose_lib.py 的优化版本

对外接口与原 choose_lib.py 完全一致，可直接替换使用：
    - 所有函数名、参数名、模块级变量名均保持不变
    - 抽卡概率、颜色标记、返回格式等行为保持一致
    - gl / nomal / custom 的随机调用顺序与原版一致，相同随机种子下结果与原版完全相同
    - ba / bac 已修复“九蓝一金”导致抽卡次数超出设定值的 BUG（见优化点 7）；
      ab < 10 时与原版逐位一致，ab >= 10 时保证结果条数恰好等于 ab

主要优化点：
    1. 移除未使用的 import（tkinter / sys / os），加快模块加载
    2. 卡池数据由 list 改为 tuple（不可变，内容不变，防止被意外修改）
    3. 成员判断改用 frozenset，由 O(n) 扫描降为 O(1) 查找
    4. 抽取公共的“九蓝一金”与“学号抽卡”逻辑，消除 gl / ba 之间的大量重复代码
    5. 补充类型注解、文档字符串与概率注释，便于后续调整
    6. 修复 s3 中 '鹤城''亚子' 缺少逗号的问题（原会被拼接成 '鹤城亚子' 一个名字，
       现拆分为 '鹤城' 与 '亚子' 两个名字；如需完全保持旧数据可自行改回）
    7. 修复 BA 模式（ba / bac）抽卡次数与设定值不符的 BUG：
       原判定 ab+1-i>=10 中，ba 的 i 从未自增、bac 存在差一错误，
       导致“九蓝一金”的 10 连抽可能使结果条数超出设定的 ab；
       现改为 len(rt1) + 10 <= ab，保证返回结果条数恰好等于 ab
       （九蓝一金仍会正常触发，只是不再超额）
"""

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

# ============================ 内部工具 ============================
# 供成员判断使用的 frozenset（O(1) 查找；仅内部使用，不影响原有变量名）
_xdwx_set = frozenset(xdwx)
_ycwx_set = frozenset(ycwx)
_xdycwx2_set = frozenset(xdycwx2)
_sx_set = frozenset(sx)
_sanx_set = frozenset(sanx)


def _append_nine_blue_one_gold(rt1: list, rt2: list, blue_pool: tuple, gold_pool: tuple) -> None:
    """九蓝一金：追加 9 个蓝色 + 1 个金色（抽数计数由调用方另行处理）。"""
    for _ in range(9):
        rt1.append(str(random.choice(blue_pool)))
        rt2.append("blue")
    rt1.append(str(random.choice(gold_pool)))
    rt2.append("yellow")


def _draw_student_numbers(ab: int, max_n: int, high_color: str, sx_color: str,
                          fallback_pool, blue_gold_pools=None,
                          checkbuttons2: int = 0) -> tuple:
    """通用“学号抽卡”引擎（gl 与 ba 共用，分支顺序与原版一致）。

    规则说明（与原版 gl 完全一致；ba 的 s==50 分支已修正超额 BUG）：
        - 抽到 xdwx 学号：再掷 1~9，偶数(4/9) 出 xdwx 池，奇数(5/9) 出 czwx 池
        - 抽到 ycwx 学号：再掷 1~10，3 的倍数(3/10) 出 ycwx 池，否则出 czwx 池
        - 抽到 xdycwx2 学号：再掷 1~10，3 的倍数(3/10) 出 xdycwx 池，否则出 czwx 池
        - 抽到 sx 学号：直接输出该学号
        - 抽到 sanx 学号：直接输出该学号
        - s == 50（仅 ba，blue_gold_pools 不为空时）：剩余条数足够容纳 10 连时触发
          九蓝一金（9 蓝 + 1 金），否则退化为单抽蓝，保证总条数恰好等于 ab
        - s == 51（仅 ba）：checkbuttons2 开启时输出 "mind maneger"，否则从 sx 池抽取
        - 其余学号：gl 从 fallback_pool 抽取；ba（fallback_pool 为 None）不产出、继续抽

    参数:
        ab: 需要抽取的个数
        max_n: 随机数上限（gl 为 49，ba 为 51）
        high_color: xdwx / ycwx / xdycwx2 分支的颜色（gl 为 yellow，ba 为 magenta）
        sx_color: 命中 sx 学号的颜色（gl 为 magenta，ba 为 yellow）
        fallback_pool: 其余数字的抽取池（ba 传 None 表示不产出）
        blue_gold_pools: (蓝池, 金池)，仅 ba 的 s==50 分支使用
        checkbuttons2: 是否启用 "mind maneger" 特殊结果
    """
    rt1 = []
    rt2 = []
    while len(rt1) < ab:
        s = random.randint(1, max_n)
        if s in _xdwx_set:
            p = random.randint(1, 9)
            rt1.append(str(random.choice(xdwx if p % 2 == 0 else czwx)))
            rt2.append(high_color)
        elif s in _sx_set:
            rt1.append(str(s))
            rt2.append(sx_color)
        elif s in _sanx_set:
            rt1.append(str(s))
            rt2.append("blue")
        elif s in _ycwx_set:
            p = random.randint(1, 10)
            rt1.append(str(random.choice(ycwx if p % 3 == 0 else czwx)))
            rt2.append(high_color)
        elif s in _xdycwx2_set:
            p = random.randint(1, 10)
            rt1.append(str(random.choice(xdycwx if p % 3 == 0 else czwx)))
            rt2.append(high_color)
        elif s == 50 and blue_gold_pools is not None:
            # 九蓝一金（仅 ba；gl 的随机数上限为 49，不会命中）
            # 修复：仅当剩余条数足够容纳完整 10 连（9 蓝 + 1 金）时才触发，
            # 否则退化为单抽蓝，保证结果条数恰好等于 ab（原版会超出设定值）
            if len(rt1) + 10 <= ab:
                _append_nine_blue_one_gold(rt1, rt2, blue_gold_pools[0], blue_gold_pools[1])
            else:
                rt1.append(str(random.choice(blue_gold_pools[0])))
                rt2.append("blue")
        elif s == 51 and blue_gold_pools is not None:
            if checkbuttons2 == 1:
                rt1.append("mind maneger")
                rt2.append("mind maneger")
            else:
                rt1.append(str(random.choice(sx)))
                rt2.append("yellow")
        elif fallback_pool is not None:
            # 原版 gl 的 else 分支：其余数字从二星池抽取
            rt1.append(str(random.choice(fallback_pool)))
            rt2.append("blue")
        # 其余情况（ba 中 9/11/29/32 等无规则学号）：不产出，继续抽取（与原版一致）
    return rt1, rt2


# ============================ 对外接口 ============================
def gl(ab: int) -> tuple:
    '''原神模式抽学号'''
    return _draw_student_numbers(ab, max_n=49, high_color="yellow",
                                 sx_color="magenta", fallback_pool=sanx)


def bac(ab: int, checkbuttons2: int) -> tuple:
    '''蔚蓝档案角色抽卡（已修复：结果条数恰好等于 ab，不再超额）'''
    rt1 = []
    rt2 = []
    i = 0
    while i < ab:
        s = random.randint(1, 51)
        if s < 10:
            # 高稀有度：偶数(4/9) 出三星，奇数(5/9) 出二星（颜色均为 magenta）
            p = random.randint(1, 9)
            rt1.append(str(random.choice(s3 if p % 2 == 0 else s2)))
            rt2.append("magenta")
        elif s < 25:  # 10 <= s < 25
            rt1.append(str(random.choice(s2)))
            rt2.append("yellow")
        elif s <= 49:  # 25 <= s <= 49
            rt1.append(str(random.choice(s2)))
            rt2.append("blue")
        elif s == 50:
            # 九蓝一金：仅当剩余条数足够容纳 10 连时才触发
            # （修复原版 ab+1-i>=10 的差一错误导致的超额；此处 i 恒等于 len(rt1)）
            if len(rt1) + 10 <= ab:
                _append_nine_blue_one_gold(rt1, rt2, s1, s2)
                i += 9
            else:
                rt1.append(str(random.choice(s1)))
                rt2.append("blue")
        else:  # s == 51
            if checkbuttons2 == 1:
                rt1.append("mind maneger")
                rt2.append("mind maneger")
            else:
                rt1.append(str(random.choice(s2)))
                rt2.append("yellow")
        i += 1
    return rt1, rt2


def ba(ab: int, checkbuttons2: int) -> tuple:
    '''蔚蓝档案模式抽学号（已修复：结果条数恰好等于 ab，不再超额）'''
    return _draw_student_numbers(ab, max_n=51, high_color="magenta",
                                 sx_color="yellow", fallback_pool=None,
                                 blue_gold_pools=(sanx, sx),
                                 checkbuttons2=checkbuttons2)


def nomal(ab: int) -> list:
    '''正常模式抽学号'''
    return [str(random.randint(1, 50)) for _ in range(ab)]


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
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = (line.strip() if strip else line.rstrip('\n') for line in f)
            if skip_empty:
                lines = (line for line in lines if line)
            return list(lines)
    except FileNotFoundError:
        print(f"错误：找不到文件 '{file_path}'")
        return []
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return []


def custom(a: list, ab: int) -> list:
    '''自定义模式抽学号'''
    if not a:
        raise IndexError("自定义卡池为空，无法抽取")
    return [str(random.choice(a)) for _ in range(ab)]
