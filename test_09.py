import time
import os
import sys # sys.stdout.write and sys.stdout.flush can be used for more controlled printing

import appcomm.helper.sound_helper as sound_helper
import appcomm.config_class as config_class

sound = sound_helper.SoundHelper(__file__, "res/dida.mp3")
# --- 全局配置参数 ---
# ASCII艺术数字的高度和每个数字图案字符串的宽度 (包含内部留白)
DIGIT_HEIGHT = 7
DIGIT_WIDTH = 8  # 每个数字/符号的ASCII图案的固定宽度
INTER_DIGIT_SPACE = "  " # 数字与数字之间，或数字与冒号之间的空格

# --- ANSI 转义码定义颜色 ---
COLORS = {
    "RESET": "\033[0m",
    "BLACK_BG": "\033[40m", # 可选的背景色
    "RED_TEXT": "\033[91m",
    "GREEN_TEXT": "\033[92m",
    "YELLOW_TEXT": "\033[93m",
    "BLUE_TEXT": "\033[94m",
    "MAGENTA_TEXT": "\033[95m",
    "CYAN_TEXT": "\033[96m",
    "WHITE_TEXT": "\033[97m",
    "BRIGHT_RED_TEXT": "\033[1;91m", # 加粗亮红色
    "BRIGHT_GREEN_TEXT": "\033[1;92m",
    "BRIGHT_YELLOW_TEXT": "\033[1;93m",
}

# --- ASCII 艺术数字定义 ---
# 每个数字和符号都由 DIGIT_HEIGHT 行字符串组成, 每行字符串长度为 DIGIT_WIDTH
ASCII_DIGITS = {
    '0': [
        " ****** ",
        " *    * ",
        " *    * ",
        " *    * ",
        " *    * ",
        " *    * ",
        " ****** "
    ],
    '1': [
        "   **   ",
        "  ***   ",
        "   **   ",
        "   **   ",
        "   **   ",
        "   **   ",
        " ****** "
    ],
    '2': [
        " ****** ",
        "      * ",
        "      * ",
        " ****** ",
        " *      ",
        " *      ",
        " ****** "
    ],
    '3': [
        " ****** ",
        "      * ",
        "      * ",
        " ****** ",
        "      * ",
        "      * ",
        " ****** "
    ],
    '4': [
        " *    * ",
        " *    * ",
        " *    * ",
        " ****** ",
        "      * ",
        "      * ",
        "      * "
    ],
    '5': [
        " ****** ",
        " *      ",
        " *      ",
        " ****** ",
        "      * ",
        "      * ",
        " ****** "
    ],
    '6': [
        " ****** ",
        " *      ",
        " *      ",
        " ****** ",
        " *    * ",
        " *    * ",
        " ****** "
    ],
    '7': [
        " ****** ",
        "      * ",
        "     *  ",
        "    *   ",
        "   *    ",
        "  *     ",
        "  *     "
    ],
    '8': [
        " ****** ",
        " *    * ",
        " *    * ",
        " ****** ",
        " *    * ",
        " *    * ",
        " ****** "
    ],
    '9': [
        " ****** ",
        " *    * ",
        " *    * ",
        " ****** ",
        "      * ",
        "      * ",
        " ****** "
    ],
    ':': [ # 普通冒号
        "        ",
        "   HH   ",
        "   HH   ",
        "        ",
        "   HH   ",
        "   HH   ",
        "        "
    ],
    ';': [ # 用于冒号闪烁的“暗”状态，或者用空格字符代替
        "        ",
        "   hh   ", # 使用小写h或.来表示暗一些
        "   hh   ",
        "        ",
        "   hh   ",
        "   hh   ",
        "        "
    ],
    ' ': [ # 完全空白的冒号，用于闪烁效果
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        "
    ]
}

# --- 工具函数 ---
def clear_screen():
    """清空终端屏幕。"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_time_input():
    """
    获取用户输入的倒计时时间 (分钟和秒)。
    返回:
        int: 总计倒计时秒数。
    """
    while True:
        try:
            print(f"{COLORS['CYAN_TEXT']}设置倒计时时间:{COLORS['RESET']}")
            minutes_str = input(f"  请输入分钟数 (0-99): {COLORS['YELLOW_TEXT']}")
            seconds_str = input(f"{COLORS['RESET']}  请输入秒数 (0-59): {COLORS['YELLOW_TEXT']}")
            print(COLORS['RESET'], end="") # 重置颜色并确保在同一行

            minutes = int(minutes_str)
            seconds = int(seconds_str)

            if not (0 <= minutes <= 99 and 0 <= seconds <= 59):
                print(f"{COLORS['RED_TEXT']}错误: 分钟数必须在0-99之间，秒数必须在0-59之间。请重新输入。{COLORS['RESET']}\n")
                continue
            
            total_seconds = minutes * 60 + seconds
            if total_seconds <= 0:
                print(f"{COLORS['RED_TEXT']}错误: 总时间必须大于0秒。请重新输入。{COLORS['RESET']}\n")
                continue
            return total_seconds
        except ValueError:
            print(f"{COLORS['RED_TEXT']}错误: 请输入有效的数字。{COLORS['RESET']}\n")

def display_large_time(total_seconds, blink_colon_state):
    """
    在屏幕上以大号ASCII艺术字显示格式化的时间。
    参数:
        total_seconds (int): 剩余的总秒数。
        blink_colon_state (bool): True 表示冒号显示为':'，False 显示为' '或';' (闪烁效果)。
    """
    if total_seconds < 0: total_seconds = 0 # 避免显示负数

    # 将总秒数转换为分钟和秒
    display_minutes = total_seconds // 60
    display_seconds = total_seconds % 60

    # 格式化为两位数的字符串，例如 7 -> "07"
    m_str = f"{display_minutes:02d}"
    s_str = f"{display_seconds:02d}"

    # 根据剩余时间选择颜色
    current_color = COLORS["BRIGHT_GREEN_TEXT"] # 默认绿色
    if total_seconds <= 10:
        current_color = COLORS["BRIGHT_RED_TEXT"] # 最后10秒红色
    elif total_seconds <= 30:
        current_color = COLORS["BRIGHT_YELLOW_TEXT"] # 30秒内黄色

    # 获取各部分数字的ASCII艺术图案
    m1_art = ASCII_DIGITS[m_str[0]]
    m2_art = ASCII_DIGITS[m_str[1]]
    s1_art = ASCII_DIGITS[s_str[0]]
    s2_art = ASCII_DIGITS[s_str[1]]

    # 根据闪烁状态选择冒号的图案
    # colon_char_key = ':' if blink_colon_state else ' ' # 完全消失的冒号
    colon_char_key = ':' if blink_colon_state else ';' # 稍微暗淡的冒号
    colon_art = ASCII_DIGITS[colon_char_key]
    
    # 准备在终端打印的内容
    output_lines = []
    title = "⏰ 滴答倒计时器 ⏰"
    title_colored = f"{COLORS['MAGENTA_TEXT']}{title.center(DIGIT_WIDTH * 5 + len(INTER_DIGIT_SPACE) * 4)}{COLORS['RESET']}"
    output_lines.append(title_colored)
    output_lines.append("") # 空一行

    # 逐行构建大数字显示
    for i in range(DIGIT_HEIGHT):
        line = current_color # 应用当前颜色
        line += m1_art[i]
        line += INTER_DIGIT_SPACE
        line += m2_art[i]
        line += INTER_DIGIT_SPACE
        line += colon_art[i] # 冒号也应用整体颜色
        line += INTER_DIGIT_SPACE
        line += s1_art[i]
        line += INTER_DIGIT_SPACE
        line += s2_art[i]
        line += COLORS["RESET"] # 在每行末尾重置颜色
        output_lines.append(line)
    
    output_lines.append("") # 空一行
    # 添加一个简单的进度条效果
    # progress_total_width = DIGIT_WIDTH * 5 + len(INTER_DIGIT_SPACE) * 4 - 4 # 总宽度减去括号和空格
    # filled_chars = int((initial_total_seconds - total_seconds) / initial_total_seconds * progress_total_width) if initial_total_seconds > 0 else 0
    # progress_bar = f"[{'#' * filled_chars}{'-' * (progress_total_width - filled_chars)}]"
    # output_lines.append(progress_bar.center(DIGIT_WIDTH * 5 + len(INTER_DIGIT_SPACE) * 4))


    # 一次性打印所有行，以减少闪烁 (但清屏还是主要原因)
    clear_screen()
    # print(COLORS.get("BLACK_BG", "")) # 可选：设置整个背景色
    for line_to_print in output_lines:
        print(line_to_print)
    # print(COLORS["RESET"]) # 确保在最后重置

def times_up_animation():
    """
    显示“时间到！”的动画效果。
    """
    clear_screen()
    message = "TIME'S UP!"
    frames = 10 # 动画帧数 (闪烁次数)

    # 定义一些用于“爆炸”效果的字符和颜色
    explosion_chars = ['*', '+', 'o', 'O', '@', '#']
    explosion_colors = [COLORS["BRIGHT_RED_TEXT"], COLORS["BRIGHT_YELLOW_TEXT"], COLORS["WHITE_TEXT"], COLORS["CYAN_TEXT"]]

    screen_center_y = DIGIT_HEIGHT // 2 + 2 # 大约在原计时器数字的中心
    screen_center_x_offset = (DIGIT_WIDTH * 5 + len(INTER_DIGIT_SPACE) * 4) // 2 # 计时器显示区域的中心偏移

    for i in range(frames):
        clear_screen()
        
        # 1. 闪烁的 "TIME'S UP!" 文本
        # 交替使用颜色
        text_color = COLORS["BRIGHT_RED_TEXT"] if i % 2 == 0 else COLORS["WHITE_TEXT"]
        
        # 简单的文本大小变化效果
        if i < frames / 2:
            padding = " " * (frames // 2 - 1 - i) # 两边空格逐渐减少
            spaced_message = padding + " ".join(list(message)) + padding
        else:
            padding = " " * (i - frames // 2)
            spaced_message = padding + " ".join(list(message)).upper() + padding


        # 打印文本，尝试使其大致居中
        # (DIGIT_HEIGHT / 2) gives approx vertical center for where time was
        for _ in range(screen_center_y - 2): print() # 向上推一些空行
        
        # 尝试打印一些随机的“火花”背景
        # 仅在文本周围的几行打印
        for r in range(5): # 火花显示5行
            line = ""
            if r == 2: # 中间行打印消息
                 # 确保消息不会太长以至于换行
                max_msg_len = (DIGIT_WIDTH * 5 + len(INTER_DIGIT_SPACE) * 4) - 4
                display_msg = (text_color + spaced_message + COLORS["RESET"])
                line = display_msg.center(max_msg_len + len(text_color) + len(COLORS["RESET"]))
            else: # 上下行打印火花
                for _ in range((DIGIT_WIDTH * 5 + len(INTER_DIGIT_SPACE) * 4) // 2): # 火花密度
                    if random.random() < 0.15: # 15%的几率出现火花
                        line += random.choice(explosion_colors) + random.choice(explosion_chars) + COLORS["RESET"]
                    else:
                        line += " "
            print(line.center( (DIGIT_WIDTH * 5 + len(INTER_DIGIT_SPACE) * 4) + 20 )) # 整体再居中一点

        for _ in range(DIGIT_HEIGHT - screen_center_y +1): print() # 向下推一些空行

        sys.stdout.flush() # 强制刷新输出，确保动画即时显示
        time.sleep(0.3) # 动画帧之间的延迟

    # 最终的固定消息
    clear_screen()
    final_lines = [
        "*************************************",
        "* *",
        "* TIME'S UP!              *",
        "* *",
        "*************************************"
    ]
    print("\n\n\n")
    for line in final_lines:
        print(f"{COLORS['BRIGHT_YELLOW_TEXT']}{line.center(80)}{COLORS['RESET']}")
    print("\n\n")
    print(f"{COLORS['CYAN_TEXT']}{'按 Enter 键退出...'.center(80)}{COLORS['RESET']}")
    input() # 等待用户按Enter退出


# --- 主程序 ---
if __name__ == "__main__":
    # 提示信息
    clear_screen()
    print(f"{COLORS['CYAN_TEXT']}欢迎使用“滴答倒计时器”！{COLORS['RESET']}")
    print("本程序将在终端中显示一个大号的倒计时时钟。")
    print("请确保您的终端支持 ANSI 颜色代码以获得最佳视觉效果。")
    print("-" * 40)
    
    initial_total_seconds = get_user_time_input() # 获取用户输入
    remaining_seconds = initial_total_seconds
    
    colon_is_visible = True # 用于控制冒号闪烁的状态

    try:
        while remaining_seconds >= 0:
            display_large_time(remaining_seconds, colon_is_visible)
            sound.play(volume=0.2, loops=-1)
            
            # 简单的“滴答”声提示 (如果想加入声音，需要额外库如playsound)
            # print("\a", end="") # BEL character, 会发出哔声，但可能很烦人或无效
            # sys.stdout.flush() # 确保提示音(如果用BEL)即时发出

            time.sleep(1.0) # 等待1秒
            
            remaining_seconds -= 1
            colon_is_visible = not colon_is_visible # 切换冒号的闪烁状态
        
        # 倒计时结束
        times_up_animation()

    except KeyboardInterrupt:
        # 用户按下 Ctrl+C
        clear_screen()
        print(f"\n{COLORS['YELLOW_TEXT']}倒计时被用户中断。下次再见！{COLORS['RESET']}\n")
    finally:
        # 确保退出时颜色被重置
        print(COLORS["RESET"])