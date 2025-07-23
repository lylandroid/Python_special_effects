# -----------------------------------------------------------
# Python 创意特效：闪电一击
#
# 教学目标：
# 1. 学习如何生成随机数来控制图形的形状。
# 2. 理解如何用一个点列表来定义和绘制一个复杂的线条（闪电）。
# 3. 学习如何创建分支，让闪电效果更逼真。
# 4. 探索如何通过背景闪烁来增强视觉冲击力。
#
# 运行方式：
# - 安装 Python 和 Pygame。
# - 将此代码保存为 a_lightning_strike.py 文件。
# - 在终端或命令行中运行 `python a_lightning_strike.py`。
# - 在弹出的黑色窗口中用鼠标左键点击，即可在点击处生成一道闪电！
# -----------------------------------------------------------

import pygame
import random # 导入随机库，这是制造 "随机性" 的关键！
import math   # 导入数学库，可能会用到一些计算

# --- 第一步: 初始化 Pygame 和创建窗口 ---

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("闪电一击 - 点击鼠标召唤闪电")

# 定义一些常用的颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230) # 一种淡淡的蓝色，用于闪电颜色

# --- 第二步: 定义创建闪电的函数 ---

# 我们将把创建闪电的核心逻辑封装在一个函数里。
# 这样代码更整洁，也方便我们重复调用。
# 参数:
#   start_pos (x, y): 闪电开始的位置
#   max_length: 闪电主干的最大垂直长度
#   max_deviation: 每一段闪电的最大水平偏移量
def create_lightning(start_pos, max_length, max_deviation):
    """
    根据起始点，生成一个闪电路径的点列表。
    闪电是由一系列的点 (x, y) 连接而成的。
    """
    path = [start_pos] # 闪电路径列表，第一个点就是起始点
    current_pos = start_pos

    # 当闪电的y坐标还没有到达屏幕底部或超过最大长度时，继续生成
    while current_pos[1] < start_pos[1] + max_length and current_pos[1] < SCREEN_HEIGHT:
        # 从当前点，计算下一个点的位置
        last_x, last_y = current_pos

        # 下一个点的 y 坐标，每次向下延伸一小段随机的距离
        next_y = last_y + random.randint(10, 25)

        # 下一个点的 x 坐标，在上一段的基础上，向左或向右随机偏移
        # random.uniform(-max_deviation, max_deviation) 会生成一个带小数的随机数
        next_x = last_x + random.uniform(-max_deviation, max_deviation)

        # 确保闪电不会偏出屏幕左右边界
        next_x = max(0, min(next_x, SCREEN_WIDTH))

        # 将新生成的点添加到路径列表中
        current_pos = (next_x, next_y)
        path.append(current_pos)

        # 有一定几率，从当前点产生一个分支闪电！
        if random.randint(0, 100) > 85: # 15% 的几率产生分支
            # 递归调用 create_lightning 来创建分支
            # 分支的长度和偏移量都比主干小一些，看起来更自然
            branch = create_lightning(current_pos, max_length * 0.5, max_deviation)
            # 将分支路径合并到主路径中 (用 None 来分隔，这样绘制时就知道是另一段)
            path.append(None) # 用 None 作为标记，表示接下来是一段分支
            path.extend(branch)
            path.append(None) # 分支结束也加一个标记

    return path


# --- 第三步: 游戏主循环 ---

# 这个列表将用来存储所有需要绘制的闪电路径
# 我们可以同时存储多道闪电
lightning_bolts = []

# 用于控制背景闪烁效果的变量
flash_alpha = 0 # 闪烁的透明度，0 表示完全透明
FLASH_DURATION = 15 # 闪烁持续的帧数

clock = pygame.time.Clock()
running = True

while running:
    # --- 3.1: 事件处理 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # 清空上一道闪电
            lightning_bolts.clear()
            # 获取鼠标点击位置
            mouse_pos = pygame.mouse.get_pos()
            # 从鼠标点击位置上方一点点的地方开始生成闪电
            start_point = (mouse_pos[0], 0) # 让闪电从屏幕顶端开始
            # 创建一道新的闪电并添加到列表中
            new_bolt = create_lightning(start_point, SCREEN_HEIGHT, 15)
            lightning_bolts.append(new_bolt)
            # 同时，触发一次背景闪烁！
            flash_alpha = 255 # 将透明度设为最大（完全不透明）

    # --- 3.2: 更新状态 ---
    # 更新闪烁效果的透明度，让它随时间变淡
    if flash_alpha > 0:
        flash_alpha -= 255 / FLASH_DURATION # 每帧减少一点透明度
        flash_alpha = max(0, flash_alpha) # 确保不会小于0

    # --- 3.3: 绘制屏幕 ---
    # 先用纯黑色填充屏幕
    screen.fill(BLACK)

    # 如果需要闪烁，就在黑色背景上叠加一个半透明的白色层
    if flash_alpha > 0:
        # 创建一个和屏幕一样大的表面，并设置它的透明度
        flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        flash_surface.fill((255, 255, 255, flash_alpha))
        # 将这个闪烁表面 "贴" 在主屏幕上
        screen.blit(flash_surface, (0, 0))

    # 绘制所有闪电
    for bolt_path in lightning_bolts:
        # pygame.draw.lines 可以一次性画出由多个点连接成的线段
        # 它需要一个点的列表，并且列表中的点不能是 None
        # 所以我们需要处理一下之前为了分支而加入的 None
        points_segment = []
        for point in bolt_path:
            if point is not None:
                points_segment.append(point)
            else:
                # 遇到 None，说明一段路径结束了，把它画出来
                if len(points_segment) > 1:
                    pygame.draw.lines(screen, LIGHT_BLUE, False, points_segment, 3) # 主干粗一点
                    # 给闪电增加一点 "光晕" 效果，就是用白色再画一遍，但更细
                    pygame.draw.lines(screen, WHITE, False, points_segment, 1)
                points_segment = [] # 清空列表，准备接收下一段路径

        # 绘制最后一段路径（如果循环结束时还有未绘制的点）
        if len(points_segment) > 1:
            pygame.draw.lines(screen, LIGHT_BLUE, False, points_segment, 3)
            pygame.draw.lines(screen, WHITE, False, points_segment, 1)


    # --- 3.4: 刷新显示 ---
    pygame.display.flip()

    # --- 3.5: 控制帧率 ---
    clock.tick(60)

# --- 第四步: 退出程序 ---
pygame.quit()