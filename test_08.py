import random
import time
import os
import math # 我们将使用math.sin来创建平滑的跳舞效果

# --- 全局配置参数 ---
SCREEN_WIDTH = 78       # 屏幕的宽度 (以字符为单位)
SCREEN_HEIGHT = 22      # 屏幕的高度 (以行为单位)
MAX_NOTES = 48          # 屏幕上同时存在的最大音符数量
MIN_NOTES = 7           # 当音符数量少于此值时，会尝试添加新音符
NOTE_ADD_CHANCE = 0.5   # 在每一帧，如果音符数量低于最大值，有此概率添加新音符

FRAME_DELAY = 0.1       # 每一帧之间的延迟时间 (秒)，值越小，动画越快

# Unicode 音乐符号字符
# 重要提示: 请确保你的终端 (控制台) 设置为使用 UTF-8 编码，否则这些符号可能无法正确显示!
MUSIC_NOTES_CHARS = ['♪', '♫', '♩', '♬', '♭', '♮', '♯', 'ø'] # 添加一个装饰性音符

# 用于音符消失时的渐变效果的字符 (从可见到消失)
FADE_CHARS = ['♦', '◊', '.', ' '] # 使用菱形、小菱形、点、空格

# --- ANSI 转义码定义颜色 ---
# 这些代码可以在大多数现代终端中显示彩色文本
COLORS = {
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "MAGENTA": "\033[95m",      # 洋红色 (粉紫色)
    "CYAN": "\033[96m",         # 青色
    "WHITE": "\033[97m",
    "BRIGHT_PINK": "\033[1;95m", # 亮粉色 (通过加粗洋红色实现)
    "LIGHT_BLUE": "\033[1;94m", # 亮蓝色
    "LIME_GREEN": "\033[1;92m", # 亮绿色
    "ORANGE": "\033[38;5;208m", # 橙色 (这是一个256色代码，如果终端不支持，可能显示不正确)
    "RESET": "\033[0m"          # 重置所有颜色和样式回到终端默认
}
# 为音符准备一个颜色列表，都是比较鲜艳活泼的颜色
AVAILABLE_NOTE_COLORS = [
    COLORS["RED"], COLORS["LIME_GREEN"], COLORS["YELLOW"], COLORS["LIGHT_BLUE"],
    COLORS["BRIGHT_PINK"], COLORS["CYAN"], COLORS["WHITE"],
    COLORS.get("ORANGE", COLORS["YELLOW"]) # 尝试使用橙色，如果ORANGE定义无效(比如终端不支持256色)，则用黄色替代
]

# --- 工具函数 ---
def clear_screen():
    """清空终端屏幕。"""
    # Windows 系统使用 'cls' 命令, macOS 和 Linux 系统使用 'clear' 命令
    os.system('cls' if os.name == 'nt' else 'clear')

# --- 跳舞音符类 ---
class DancingNote:
    """
    代表一个在屏幕上跳舞的音乐音符。
    每个音符实例都会有自己的位置、外观、生命周期和独特的“舞姿”。
    """
    def __init__(self, screen_width, screen_height):
        """
        初始化一个新的跳舞音符。
        参数:
            screen_width (int): 动画区域的宽度。
            screen_height (int): 动画区域的高度。
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 1. 外观属性
        self.char = random.choice(MUSIC_NOTES_CHARS) # 从列表中随机选择一个音符字符
        self.color = random.choice(AVAILABLE_NOTE_COLORS) # 随机选择一个颜色

        # 2. 位置和移动属性
        # 初始 x 坐标，随机分布在屏幕宽度内 (留出一点边界)
        self.x = float(random.randint(1, self.screen_width - 2))
        # `base_y` 是音符垂直跳舞的基准线，或者说是它的“地板”的中心点
        # 我们希望音符主要在屏幕的中下部跳动
        self.base_y = float(random.randint(int(self.screen_height * 0.4), self.screen_height - 3))
        self.y = self.base_y # 当前的 y 坐标，初始时等于基准线

        # 3. “舞姿”参数 (我们将使用正弦函数来模拟平滑的上下跳动)
        self.amplitude = random.uniform(1.5, 4.5)  # 振幅：音符上下跳动的高度
        self.frequency = random.uniform(0.08, 0.3) # 频率：音符上下跳动的速度
        self.phase = random.uniform(0, 2 * math.pi) # 相位：确保每个音符的起始“舞步”不同

        # 水平漂移速度，让音符左右慢慢移动
        self.drift_speed_x = random.uniform(-0.6, 0.6)

        # 4. 生命周期属性
        self.age = 0 # 音符已存活的帧数
        # 音符的寿命 (总共存活多少帧)，之后会开始消失
        self.lifespan = random.randint(70, 220) # 大约 7 到 22 秒 (假设 FRAME_DELAY=0.1)
        self.is_fading = False # 标志位，表示音符是否已进入“消失”阶段

    def update(self):
        """
        更新音符在每一帧的状态 (年龄、位置、外观)。
        返回:
            bool: 如果音符仍然可见 (存活)，返回 True；否则返回 False (表示可以被移除)。
        """
        self.age += 1 # 音符年龄增加

        # --- 垂直跳舞运动 (使用正弦函数) ---
        # 公式: y = 基准线 + 振幅 * sin(频率 * 年龄 + 相位)
        # 这会使音符在 base_y 上下平滑地移动
        vertical_offset = self.amplitude * math.sin(self.frequency * self.age + self.phase)
        self.y = self.base_y + vertical_offset

        # --- 水平漂移运动 ---
        self.x += self.drift_speed_x

        # --- 边界检查 ---
        # 水平边界：如果音符漂移到屏幕边缘，让它从另一边出来 (环绕效果)
        if self.x >= self.screen_width -1 : # 超出右边界
            self.x = 0
        elif self.x < 0: # 超出左边界
            self.x = self.screen_width -1

        # 垂直边界：确保音符不会跳得太高或太低，尽量保持在屏幕内
        # (通常 base_y 和 amplitude 的设定会使其保持在合理范围)
        # 这里再加一层保护，防止极端情况
        self.y = max(1, min(self.y, self.screen_height - 2)) # 上下留出1行边距

        # --- 生命周期与消失效果 ---
        # 当音符年龄接近其寿命时，开始进入“消失”阶段
        # FADE_CHARS列表有多少个字符，就提前多少 * N 帧开始消失 (N大约是每个消失字符持续的帧数)
        fade_duration_per_char = 6 # 每个消失字符显示约6帧
        total_fade_frames = len(FADE_CHARS) * fade_duration_per_char
        
        if self.age > self.lifespan - total_fade_frames:
            self.is_fading = True

        if self.is_fading:
            # 计算当前处于消失过程的哪个阶段
            frames_into_fade = self.age - (self.lifespan - total_fade_frames)
            fade_char_index = frames_into_fade // fade_duration_per_char # 使用整数除法

            if fade_char_index < len(FADE_CHARS):
                self.char = FADE_CHARS[fade_char_index] # 改变字符来模拟消失
                if self.char == ' ': # 如果字符变成了空格，说明它完全不可见了
                    return False # 标记此音符为可移除
            else:
                # 如果索引超出了FADE_CHARS列表 (理论上应该在上面一步就返回False了)
                return False # 标记此音符为可移除
        
        # 如果音符的年龄超过了其设定的寿命 (且未通过is_fading逻辑返回False)
        if self.age >= self.lifespan:
            return False # 标记此音符为可移除

        return True # 音符仍然存活且可见

    def get_draw_info(self):
        """
        获取用于在屏幕上绘制此音符所需的信息。
        返回:
            tuple: (整数x坐标, 整数y坐标, 带颜色的音符字符)
        """
        # 将浮点数坐标转换为整数，因为屏幕的单元格是离散的
        draw_x = int(self.x)
        draw_y = int(self.y)
        
        # 组合颜色代码、音符字符和重置代码，形成最终要打印的字符串
        colored_char_string = f"{self.color}{self.char}{COLORS['RESET']}"
        
        return draw_x, draw_y, colored_char_string

# --- 主动画循环 ---
def main_animation_loop():
    """
    运行“跳舞音符”动画的主循环。
    """
    active_notes = [] # 一个列表，用于存放所有当前在屏幕上活动的DancingNote对象

    # 动画开始时，先创建一些初始的音符
    # 数量在 MIN_NOTES 和 MAX_NOTES/2 之间随机
    for _ in range(random.randint(MIN_NOTES, MAX_NOTES // 2 + 1)):
        active_notes.append(DancingNote(SCREEN_WIDTH, SCREEN_HEIGHT))

    try:
        while True: # 无限循环，直到用户中断 (Ctrl+C)
            # --- 1. 添加新的音符 ---
            # 如果当前音符数量少于设定的最大值，并且随机数满足添加概率，
            # 或者当前音符数量低于最小值，就尝试添加新音符。
            should_add_note = (len(active_notes) < MAX_NOTES and random.random() < NOTE_ADD_CHANCE) or \
                              (len(active_notes) < MIN_NOTES)
            
            if should_add_note and len(active_notes) < MAX_NOTES : # 再次确认不超过最大值
                active_notes.append(DancingNote(SCREEN_WIDTH, SCREEN_HEIGHT))

            # --- 2. 更新所有活动音符的状态 ---
            notes_to_keep_this_frame = [] # 临时列表，存放本帧更新后仍然存活的音符
            for note in active_notes:
                if note.update(): # 调用每个音符的update方法
                    notes_to_keep_this_frame.append(note) # 如果update返回True，则保留此音符
            active_notes = notes_to_keep_this_frame # 用更新后的列表替换旧列表

            # --- 3. 准备绘制屏幕 ---
            # 创建一个空白的屏幕缓冲区 (一个二维列表，代表屏幕的每个字符位置)
            # 我们将先把所有内容画到这个缓冲区，再一次性打印出来，以减少闪烁
            screen_buffer = [[' ' for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

            # 将每个活动音符“画”到屏幕缓冲区上
            for note in active_notes:
                nx, ny, nchar_colored = note.get_draw_info() # 获取音符的绘制信息
                
                # 确保音符的绘制坐标在屏幕的有效范围内
                if 0 <= ny < SCREEN_HEIGHT and 0 <= nx < SCREEN_WIDTH:
                    # 将带颜色的音符字符放到缓冲区的对应位置
                    # 注意：如果多个音符重叠在同一位置，后画的会覆盖先画的
                    screen_buffer[ny][nx] = nchar_colored
            
            # --- 4. 渲染（打印）整个帧 ---
            clear_screen() # 清空上一个旧的帧内容

            # 打印动画标题
            # 为了让标题居中，我们需要考虑ANSI颜色代码不占显示宽度的问题
            # 简单处理：给center的宽度参数增加颜色代码的长度
            title_text = "♪♫♩♬  跳舞的音符 - Dancing Notes! ♬♩♫♪"
            colored_title = f"{COLORS['MAGENTA']}{title_text}{COLORS['RESET']}"
            title_padding = len(COLORS['MAGENTA']) + len(COLORS['RESET'])
            print(colored_title.center(SCREEN_WIDTH + title_padding))
            
            # 打印一个简单的顶部边框
            print(f"{COLORS['CYAN']}{'-' * SCREEN_WIDTH}{COLORS['RESET']}")

            # 逐行打印屏幕缓冲区的内容
            for row_index in range(SCREEN_HEIGHT):
                print("".join(screen_buffer[row_index]))

            # 打印一个简单的底部边框
            print(f"{COLORS['CYAN']}{'-' * SCREEN_WIDTH}{COLORS['RESET']}")
            # 打印提示信息和当前音符数量
            status_text = f"按 Ctrl+C 退出.  当前音符数量: {len(active_notes)}"
            colored_status = f"{COLORS['YELLOW']}{status_text}{COLORS['RESET']}"
            status_padding = len(COLORS['YELLOW']) + len(COLORS['RESET'])
            # 使用ljust让状态信息靠左，并填满宽度
            print(colored_status.ljust(SCREEN_WIDTH + status_padding))


            # --- 5. 控制动画速度 ---
            time.sleep(FRAME_DELAY) # 暂停一小段时间，然后进入下一帧

    except KeyboardInterrupt:
        # 当用户按下 Ctrl+C 时，会触发 KeyboardInterrupt 异常
        clear_screen() # 清理屏幕
        # 打印一个友好的退出消息
        print(f"\n{COLORS['GREEN']}感谢欣赏这场音符的舞蹈！期待下次与你相遇！ 👋{COLORS['RESET']}\n")
    finally:
        # `finally`块中的代码无论如何都会执行 (正常退出或异常退出)
        # 在这里确保终端的颜色被重置回默认状态，以防程序意外退出导致颜色混乱
        print(COLORS['RESET'])

if __name__ == "__main__":
    # 程序入口点
    # 打印一些启动提示信息
    print("正在启动“跳舞的音符”动画程序...")
    print("温馨提示:")
    print("  1. 请确保您的终端 (控制台) 支持 Unicode (UTF-8) 字符，否则音符可能显示为问号或乱码。")
    print("  2. 同时，终端需要支持 ANSI 颜色代码才能看到五彩斑斓的效果哦！")
    print("  3. 如果动画看起来太快或太慢，可以调整代码中的 `FRAME_DELAY` 值。")
    print("  (动画将在几秒后开始...)")
    time.sleep(3) # 等待几秒，让用户有机会阅读提示

    main_animation_loop() # 开始动画主循环