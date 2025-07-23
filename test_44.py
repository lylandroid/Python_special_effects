# -----------------------------------------------------------
# Python 创意特效：涟漪效应
#
# 教学目标：
# 1. 学习使用 Pygame 库创建一个窗口。
# 2. 理解基本的事件处理（如鼠标点击和关闭窗口）。
# 3. 学习如何使用类 (class) 来管理多个对象（涟漪）。
# 4. 探索如何通过改变颜色、半径和透明度来创建动画效果。
#
# 运行方式：
# - 安装 Python 和 Pygame。
# - 将此代码保存为 a_ripple_effect.py 文件。
# - 在终端或命令行中运行 `python a_ripple_effect.py`。
# - 在弹出的黑色窗口中用鼠标左键点击，即可看到涟漪效果！
# -----------------------------------------------------------

import pygame
import math # 导入数学库，用于计算颜色等

# --- 第一步: 初始化 Pygame 和创建窗口 ---

# 初始化 Pygame 的所有模块，这是每个 Pygame 程序的必须步骤
pygame.init()

# 设置窗口的宽度和高度（单位是像素）
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 使用设置好的宽度和高度创建一个窗口，并赋值给 screen 变量
# screen 就好比是我们的画布，我们将在上面绘制所有东西
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 设置窗口的标题
pygame.display.set_caption("涟漪效应 - 点击鼠标创造水波纹")

# 定义一些常用的颜色 (使用 RGB 颜色模式)
BLACK = (0, 0, 0)         # 背景色：黑色
WHITE = (255, 255, 255)   # 初始涟漪颜色：白色

# --- 第二步: 创建一个涟漪 "类" (Class) ---

# "类" 就像一个蓝图或模板，我们可以用它来创建很多个相似但又独立的对象。
# 在这里，我们用它来创建每一圈的涟漪。
class Ripple:
    # 这是类的 "构造函数" 或 "初始化方法"。
    # 当我们创建一个新的 Ripple 对象时，这个方法会被自动调用。
    # 它需要知道涟漪的中心位置 (x, y)。
    def __init__(self, x, y):
        # 记录涟漪的中心点坐标
        self.x = x
        self.y = y
        # 涟漪的初始半径，从0开始慢慢变大
        self.radius = 0
        # 涟漪的宽度，我们让它保持不变
        self.width = 3
        # 涟漪的颜色，我们让它从白色开始
        self.color = WHITE
        # 涟漪的 "生命值" 或 "年龄"，用于之后计算透明度
        self.age = 0

    # 这个方法用来更新涟漪的状态（让它变大、变淡）
    def update(self):
        # 每次更新，半径增加一点点，这样看起来就像在扩散
        self.radius += 1.5

        # 每次更新，"年龄" 也增加一点
        self.age += 1

        # 当涟漪变得太大时，我们就不再需要它了。
        # 这个方法会返回 True 如果涟漪还 "活着"，返回 False 如果它该 "消失" 了。
        if self.age > 120: # 这个数值可以调整，数值越大，涟漪持续时间越长
            return False
        return True

    # 这个方法用来把涟漪画在屏幕上
    def draw(self, surface):
        # 我们希望涟漪越到后面越透明，模拟消失的效果。
        # 我们通过年龄来计算一个 alpha (透明度) 值。
        # age 越大, alpha 越小 (越透明)。
        # max(0, ...) 确保 alpha 不会变成负数。
        alpha = max(0, 255 - self.age * 2)

        # Pygame 画圆时不支持直接设置透明度，所以我们创建一个临时的 "表面" (Surface)
        # 这个表面的大小刚好能容纳我们的圆环。
        # SRCALPHA 标志让这个表面支持 "alpha通道"（即透明度）。
        ripple_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)

        # 在这个临时的表面上画一个圆。
        # 参数分别是：画在哪里，颜色(R, G, B, Alpha)，圆心，半径，线宽。
        pygame.draw.circle(
            ripple_surface,
            (self.color[0], self.color[1], self.color[2], alpha), # 颜色加上了透明度
            (self.radius, self.radius), # 圆心在这个临时表面的中心
            self.radius,
            self.width
        )

        # 最后，把这个画好了带透明圆环的临时表面，"贴" 到我们的主屏幕 (surface) 上。
        # 我们需要计算好粘贴的左上角位置，以确保圆环的中心在我们想要的地方。
        surface.blit(ripple_surface, (self.x - self.radius, self.y - self.radius))

# --- 第三步: 游戏主循环 ---

# 创建一个空列表，用来存放所有 "活着" 的涟漪对象
ripples = []

# 创建一个时钟对象，它可以帮助我们控制游戏的帧率 (FPS)
clock = pygame.time.Clock()

# running 变量用来控制主循环是否继续运行
running = True

# 这是程序的核心部分，一个 "while" 循环。
# 只要 running 是 True，这个循环就会一直执行下去。
while running:
    # --- 3.1: 事件处理 ---
    # pygame.event.get() 会获取所有用户操作（比如按键盘、点鼠标）
    for event in pygame.event.get():
        # 如果用户点击了窗口的关闭按钮
        if event.type == pygame.QUIT:
            running = False # 将 running 设为 False，循环将在下次检查时停止

        # 如果用户按下了鼠标按键
        if event.type == pygame.MOUSEBUTTONDOWN:
            # pygame.mouse.get_pressed() 会返回 (左键, 中键, 右键) 的状态
            # 我们只关心左键，所以检查第一个元素 [0]
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标点击的位置 (x, y)
                pos = pygame.mouse.get_pos()
                # 使用这个位置，创建一个新的 Ripple 对象
                new_ripple = Ripple(pos[0], pos[1])
                # 将这个新的涟漪添加到我们的涟漪列表中
                ripples.append(new_ripple)

    # --- 3.2: 更新状态 ---
    # 我们创建一个新的列表，只保留那些还 "活着" 的涟漪
    # 这是一个高效的方式来移除那些已经 "老去" 的涟漪
    living_ripples = []
    for ripple in ripples:
        if ripple.update(): # 调用每个涟漪的 update 方法
            living_ripples.append(ripple) # 如果 update 返回 True，就保留它
    ripples = living_ripples # 用新的列表替换旧的列表

    # --- 3.3: 绘制屏幕 ---
    # 用纯黑色填充整个屏幕，这会清除上一帧画的所有内容
    screen.fill(BLACK)

    # 遍历所有 "活着" 的涟漪
    for ripple in ripples:
        ripple.draw(screen) # 调用每个涟漪的 draw 方法，把它画在屏幕上

    # --- 3.4: 刷新显示 ---
    # 当所有东西都画好后，调用这个函数来把 "幕后" 的画布更新到屏幕上，让玩家看到。
    pygame.display.flip()

    # --- 3.5: 控制帧率 ---
    # clock.tick(60) 会让循环每秒最多运行 60 次。
    # 这可以防止程序运行得太快，并使得动画在不同性能的电脑上看起来速度一致。
    clock.tick(60)

# --- 第四步: 退出程序 ---

# 当 `running` 变为 `False`，循环结束，程序会执行到这里。
# 调用 quit() 函数来卸载 Pygame 模块，清理资源。
pygame.quit()