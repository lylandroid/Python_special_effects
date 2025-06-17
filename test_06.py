import time  # 用来控制打字的速度，制造延迟效果
import sys   # 用来直接控制输出，比如不换行打印字符
import random # 用来产生随机数，让打字效果更自然、颜色更多变

# --- 颜色定义 (ANSI 转义码) ---
# 这些特殊的字符串告诉你的电脑终端（显示文字的地方）改变文字的颜色或样式。
# 例如: print(COLORS["PINK"] + "这段文字是粉色的!" + COLORS["ENDC"])
# '\033[' 是一个控制序列的开始，'m' 是结束。中间的数字代表不同的颜色或样式。
# 'ENDC' (End Character) 非常重要，它会把颜色恢复成默认，不然之后所有的文字都会是最后设置的颜色。
COLORS = {
    "PINK": "\033[95m",       # 亮洋红色 (就像鲜艳的粉红色)
    "BLUE": "\033[94m",       # 亮蓝色
    "CYAN": "\033[96m",       # 亮青色 (像浅蓝色和绿色的混合)
    "GREEN": "\033[92m",      # 亮绿色
    "YELLOW": "\033[93m",     # 亮黄色
    "RED": "\033[91m",        # 亮红色
    "BOLD": "\033[1m",        # 文字加粗
    "UNDERLINE": "\033[4m",   # 文字加下划线
    "ENDC": "\033[0m"         # 结束颜色/样式设置，恢复默认
}

# 预设一些好看的颜色组合，打字机可以从中随机挑选
FUN_COLORS_LIST = [COLORS["PINK"], COLORS["BLUE"], COLORS["CYAN"], COLORS["GREEN"], COLORS["YELLOW"], COLORS["RED"]]

def typewriter_magic(
    text_to_print,          # 要在屏幕上打印的文本内容
    base_char_delay=0.08,   # 每个字符之间基础的等待时间（单位：秒）。数值越小，打字越快。
    random_delay_factor=0.5,# 给打字速度增加一点随机性 (0.0 到 1.0之间)。
                            # 0.0 表示速度完全固定。
                            # 0.5 表示实际等待时间会在基础时间的50%到150%之间变化。
    cursor_symbol="▋",      # 显示在当前打字位置的光标符号，比如 "▋", "|", "_", "*"
    use_fun_colors=True,    # 是否为每个打印的字符随机选择一个鲜艳的颜色
    fixed_color_key=None    # 如果 use_fun_colors 设置为 False，这里可以指定一个固定的颜色。
                            # 例如，填入 "GREEN" (必须是上面COLORS字典里定义好的键名)。
                            # 如果为 None，则使用终端的默认颜色。
):
    """
    ✨ 打字机魔术函数 ✨
    这个函数会在终端上逐个字符地打印出你给它的文本，
    模拟老式打字机打字的效果，并且可以加上彩色的文字和移动的光标，看起来非常酷！
    """

    # --- 准备工作：计算延迟时间 ---
    # 为了让打字效果不那么死板，我们让每次等待的时间有一点点随机变化。
    # random_delay_factor 控制了这个随机变化的范围。
    if not (0.0 <= random_delay_factor <= 1.0):
        # 如果使用者输入了一个不合理的范围，给个提示并使用一个默认值。
        print(f"{COLORS['YELLOW']}提示: random_delay_factor ({random_delay_factor}) 建议在 0.0 和 1.0 之间。已自动设为 0.5。{COLORS['ENDC']}")
        random_delay_factor = 0.5
    
    min_delay = base_char_delay * (1.0 - random_delay_factor)  # 计算最短等待时间
    max_delay = base_char_delay * (1.0 + random_delay_factor)  # 计算最长等待时间
    
    # 确保最短等待时间不会太小（比如小于0）或者等于0，至少是0.01秒，不然太快就看不清效果了。
    min_delay = max(0.01, min_delay)

    # --- 开始逐个字符打印魔术 ---
    # 'enumerate' 可以让我们在遍历文本中每个字符的同时，也知道这个字符是第几个。
    for i, character in enumerate(text_to_print):
        
        # 1. 选择当前字符要显示的颜色
        active_color_code = ""  # 先假设没有特殊颜色
        if use_fun_colors:
            # 如果开启了随机颜色，就从我们准备好的颜色列表里随便选一个
            active_color_code = random.choice(FUN_COLORS_LIST)
        elif fixed_color_key and fixed_color_key in COLORS:
            # 如果关闭了随机颜色，但指定了一个固定颜色，并且这个颜色是我们定义过的
            active_color_code = COLORS[fixed_color_key]
        
        # 把选好的颜色码写到输出中。如果 active_color_code 是空的，就什么也不做。
        sys.stdout.write(active_color_code)
        
        # 2. 打印出当前这个字符
        sys.stdout.write(character)
        
        # 3. 在当前字符后面，打印出我们的光标符号
        #    但是，如果是文本的最后一个字符，就不需要再显示光标了，因为马上要换行结束。
        if i < len(text_to_print) - 1:
            sys.stdout.write(cursor_symbol)
        
        # 4. 强制刷新输出！
        #    sys.stdout.flush() 非常重要。它告诉电脑：“立刻把我刚才让你写的东西显示出来！”
        #    没有它，电脑可能会等攒够了一堆文字才一起显示，那样就看不到逐字打印的效果了。
        sys.stdout.flush()
        
        # 5. 让程序“睡”一小会儿，制造打字的停顿感
        #    使用 random.uniform(最小值, 最大值) 来获得一个在这个范围内的随机小数作为等待时间。
        current_delay = random.uniform(min_delay, max_delay)
        time.sleep(current_delay)
        
        # 6. 清除刚才打印的光标，为下一个字符或者结束做准备
        #    这个操作只在不是最后一个字符时进行。
        #    方法：
        #    '\b' 是一个特殊的“退格符”，它会把光标往左移动一格。
        #    我们先移回去，用一个空格 ' ' 盖掉原来的光标，
        #    然后再用一个 '\b' 把光标移回到那个空格的位置。
        #    这样，下一个字符就能准确地打印在光标消失的地方了。
        if i < len(text_to_print) - 1:
            sys.stdout.write("\b" + " " + "\b") # 这是清除前一个字符（这里是光标）的常用小技巧

    # --- 文本全部打印完毕 ---
    # 7. 最后，记得把颜色设置恢复到终端的默认状态！
    sys.stdout.write(COLORS["ENDC"])
    
    # 8. 打印一个换行符，这样之后如果还有其他内容输出，会从新的一行开始。
    sys.stdout.write("\n")
    sys.stdout.flush() # 再次刷新，确保换行符也立刻生效。

# --- 主程序入口：在这里展示我们的打字机魔术！ ---
# 'if __name__ == "__main__":' 是Python程序的一个常见写法，
# 意思是：“如果这个脚本是直接被运行的（而不是被其他脚本导入的），那么就执行下面的代码。”
if __name__ == "__main__":
    print(f"{COLORS['BOLD']}{COLORS['PINK']}✨✨ 打字机魔术 - 表演开始 ✨✨{COLORS['ENDC']}")
    print("---------------------------------------\n")
    time.sleep(1) # 等待1秒，给观众一点期待感

    # 第一个例子：使用默认的随机颜色和光标
    message1 = "你好，编程小天才！🚀 欢迎来到Python的奇妙世界！"
    print(f"{COLORS['GREEN']}第一段表演 (随机颜色，默认光标 '▋'):{COLORS['ENDC']}")
    typewriter_magic(message1, base_char_delay=0.07, random_delay_factor=0.6)
    time.sleep(0.5) # 在不同段落之间稍微停一下

    # 第二个例子：使用固定的蓝色，并换一个光标符号
    message2 = "看，我可以变成蓝色的打字机！酷不酷？😎"
    print(f"\n{COLORS['BLUE']}第二段表演 (固定蓝色，光标是 '>>'):{COLORS['ENDC']}")
    typewriter_magic(message2, base_char_delay=0.06, cursor_symbol=">>", use_fun_colors=False, fixed_color_key="BLUE")
    time.sleep(0.5)

    # 第三个例子：打字速度更快，使用终端默认颜色（不加彩色），换个下划线光标
    message3 = "我还可以打字很快...快到飞起！咻咻咻~ 💨"
    print(f"\n{COLORS['YELLOW']}第三段表演 (快速，默认颜色，光标是 '_'):{COLORS['ENDC']}")
    typewriter_magic(message3, base_char_delay=0.03, random_delay_factor=0.3, cursor_symbol="_", use_fun_colors=False)
    time.sleep(0.5)

    # 第四个例子：展示如何在文本中嵌入加粗和下划线效果
    # 注意：加粗和下划线的颜色码是直接写在 message4 字符串里的。
    # typewriter_magic 函数会照常处理这些码（它们也是字符）。
    message4 = f"我们还可以用 {COLORS['BOLD']}加粗{COLORS['ENDC']} 和 {COLORS['UNDERLINE']}下划线{COLORS['ENDC']} 来强调重点哦！"
    print(f"\n{COLORS['CYAN']}第四段表演 (文本自带加粗/下划线，整体随机颜色):{COLORS['ENDC']}")
    typewriter_magic(message4, base_char_delay=0.08, use_fun_colors=True)
    time.sleep(0.5)

    # 第五个例子: 使用一个可爱的表情符号作为光标
    message5 = "编程让我们的世界更有趣！"
    print(f"\n{COLORS['RED']}最终表演 (用 '❤️' 做光标):{COLORS['ENDC']}")
    typewriter_magic(message5, base_char_delay=0.1, cursor_symbol="❤️ ", use_fun_colors=True, random_delay_factor=0.2) # 注意光标后加了个空格，让清除更容易
    # 对于某些占位宽度不一的表情符号，光标清除可能需要调整，比如用 " \b\b" 等。
    # "❤️ " 后面加空格，清除时用 "\b\b  \b\b" 可能更稳定，但简单起见，这里还是用标准方式。

    print("\n---------------------------------------")
    print(f"{COLORS['BOLD']}{COLORS['PINK']}🎉 表演结束！希望你喜欢这个打字机魔术！ 🎉{COLORS['ENDC']}")
    print(f"{COLORS['YELLOW']}小朋友，你可以试试修改代码里的这些地方：{COLORS['ENDC']}")
    print(f"{COLORS['CYAN']}- 'text_to_print' 的内容，换成你想说的话！{COLORS['ENDC']}")
    print(f"{COLORS['CYAN']}- 'base_char_delay' 的数值，调快或调慢打字速度。{COLORS['ENDC']}")
    print(f"{COLORS['CYAN']}- 'cursor_symbol' 换成你喜欢的符号。{COLORS['ENDC']}")
    print(f"{COLORS['CYAN']}- 'use_fun_colors' 和 'fixed_color_key' 改变颜色效果。{COLORS['ENDC']}")
    print(f"{COLORS['GREEN']}大胆尝试，看看你能创造出什么更有趣的效果吧！🎨{COLORS['ENDC']}")