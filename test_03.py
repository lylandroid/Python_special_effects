import pygame
import sys
import math
from appcomm.helper.font_helper import FontHelper

# 初始化 pygame
pygame.init()

# 设置窗口尺寸
width, height = 600, 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("加载中... | 脉冲进度条动画")

# 设置颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (180, 0, 255)

# 设置字体
font = FontHelper(None, None, 36)
# font = pygame.font.SysFont("Arial", 36)

# 控制帧率
clock = pygame.time.Clock()

# 小球类，用来创建和绘制加载点
class PulseBall:
    def __init__(self, x, delay):
        self.x = x              # x 坐标
        self.base_y = height // 2 + 30  # 基础 y 位置（水平线）
        self.delay = delay      # 每个小球的动画延迟
        self.radius = 10        # 小球半径

    def draw(self, surface, frame):
        # 使用正弦波函数产生跳动效果
        phase = (frame + self.delay) / 10
        y_offset = math.sin(phase) * 20  # 上下浮动范围
        y = self.base_y - y_offset

        # 渐变颜色亮度
        brightness = (math.sin(phase) + 1) / 2  # 0 到 1
        color = (
            int(PURPLE[0] * brightness),
            int(PURPLE[1] * brightness),
            int(PURPLE[2] * brightness)
        )

        pygame.draw.circle(surface, color, (self.x, int(y)), self.radius)

# 创建一组脉冲小球，依次排开
balls = []
start_x = 180
spacing = 40
for i in range(5):  # 5 个小球
    balls.append(PulseBall(start_x + i * spacing, delay=i * 5))

frame = 0
running = True
while running:
    screen.fill(BLACK)

    # 显示文字
    rect = font.render("Pthon 加载中...", WHITE)
    rect.center = (width // 2, 60)
    font.blit(screen)

    # 绘制小球动画
    for ball in balls:
        ball.draw(screen, frame)

    # 检查退出事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)
    frame += 1  # 每帧增加帧计数

pygame.quit()
sys.exit()


# import pygame
# import math
# import colorsys
# import asyncio
# import platform

# # 初始化 Pygame，用于创建动画窗口
# pygame.init()

# # 设置屏幕大小
# screen_width = 800  # 窗口宽度
# screen_height = 300  # 窗口高度
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("加载脉冲进度条")

# # 定义颜色
# black = (0, 0, 0)  # 背景颜色：黑色
# white = (255, 255, 255)  # 备用颜色：白色

# # 进度条参数
# bar_max_width = 400  # 进度条最大宽度
# bar_height = 40  # 进度条高度
# bar_x = (screen_width - bar_max_width) // 2  # 进度条水平居中
# bar_y = screen_height // 2 - bar_height // 2  # 进度条垂直居中
# pulse_speed = 0.05  # 脉冲动画速度
# hue = 0.0  # 色相值，用于颜色渐变（0.0 到 1.0）

# # 生成彩虹色的函数
# def get_rainbow_color(hue):
#     # 使用 HSV 颜色模型，生成鲜艳的颜色
#     rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)  # 饱和度和亮度设为最大
#     return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

# # 初始化设置
# def setup():
#     pass  # 已经初始化，无需额外设置

# # 主更新循环
# def update_loop():
#     global hue
#     # 处理事件，允许关闭窗口
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             if platform.system() != "Emscripten":  # 非 Pyodide 环境
#                 pygame.quit()
#                 exit()

#     # 更新色相，实现颜色渐变（从蓝色到紫色循环）
#     hue = (hue + 0.01) % 1.0
#     bar_color = get_rainbow_color(hue)

#     # 使用正弦函数计算脉冲效果，改变进度条宽度
#     pulse = math.sin(pygame.time.get_ticks() * pulse_speed)  # 正弦值在 -1 到 1 之间
#     bar_width = bar_max_width * (0.7 + 0.3 * pulse)  # 宽度在 70% 到 100% 之间变化

#     # 绘制背景（清屏）
#     screen.fill(black)

#     # 绘制进度条
#     pygame.draw.rect(screen, bar_color, (bar_x, bar_y, bar_width, bar_height), border_radius=10)

#     # 更新屏幕显示
#     pygame.display.flip()

# # 设置帧率（每秒帧数）
# FPS = 30

# # 异步主循环（适配 Pyodide）
# async def main():
#     setup()
#     while True:
#         update_loop()
#         asyncio.sleep(30.0 / FPS)
#         # await asyncio.sleep(300.0 / FPS)

# # 根据运行环境选择循环模式
# if platform.system() == "Emscripten":
#     # Pyodide 环境使用异步循环
#     asyncio.ensure_future(main())
# else:
#     # 本地运行使用标准 Pygame 循环
#     if __name__ == "__main__":
#         setup()
#         running = True
#         clock = pygame.time.Clock()
#         while running:
#             update_loop()
#             clock.tick(FPS)
#         pygame.quit()

# import pygame
# import math # 用于计算脉动效果中的正弦函数

# # --- Pygame 初始化 ---
# pygame.init()
# pygame.font.init() # 初始化字体模块，如果还没有的话

# # --- 常量定义 ---
# SCREEN_WIDTH = 800  # 屏幕宽度
# SCREEN_HEIGHT = 200 # 屏幕高度 (可以根据需要调整，进度条不需要太高)
# FPS = 60            # 动画的每秒帧数

# # 进度条尺寸和位置
# BAR_WIDTH = 600
# BAR_HEIGHT = 50
# BAR_X = (SCREEN_WIDTH - BAR_WIDTH) // 2  # 水平居中
# BAR_Y = (SCREEN_HEIGHT - BAR_HEIGHT) // 2 # 垂直居中

# # 圆角半径 (让进度条看起来更柔和)
# CORNER_RADIUS = int(BAR_HEIGHT / 2.5)

# # 颜色定义 (RGB格式)
# # 背景色 (深邃的颜色，让进度条突出)
# BACKGROUND_COLOR = (30, 30, 50)
# # 进度条轨道 (未填充部分) 的颜色
# TRACK_COLOR = (70, 70, 90)
# # 进度条填充部分的基础颜色 (例如，一种明亮的蓝色)
# FILL_BASE_COLOR = (0, 120, 255)
# # 用于脉动效果的颜色增量 (加到基础颜色上，使其变亮)
# FILL_PULSE_ADD_COLOR = (60, 60, 60)
# # 边框颜色
# BORDER_COLOR = (150, 180, 255)
# # 光泽效果的颜色 (半透明白色)
# SHEEN_COLOR = (255, 255, 255, 70) # 第四个值是alpha透明度 (0-255)
# # 文本颜色
# TEXT_COLOR = (220, 220, 240)

# # 动画参数
# PULSE_SPEED = 3.0      # 脉动动画的速度 (弧度/秒)
# SHEEN_SPEED = 200      # 光泽扫过动画的速度 (像素/秒)
# SHEEN_WIDTH = 40       # 光泽带的宽度

# # --- 屏幕和时钟设置 ---
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("加载脉冲进度条 (Loading Pulse Bar)")
# clock = pygame.time.Clock()

# # --- 字体加载 ---
# # 尝试加载一个好看的字体，如果找不到，则使用Pygame默认字体
# try:
#     progress_font = pygame.font.SysFont("Arial", int(BAR_HEIGHT * 0.6)) # 字体大小相对于条的高度
# except:
#     progress_font = pygame.font.Font(None, int(BAR_HEIGHT * 0.6)) # Pygame默认字体

# # --- 进度条类 ---
# class PulsingProgressBar:
#     def __init__(self, x, y, width, height, corner_radius):
#         """
#         初始化进度条对象。
#         :param x: 进度条左上角 x 坐标
#         :param y: 进度条左上角 y 坐标
#         :param width: 进度条总宽度
#         :param height: 进度条总高度
#         :param corner_radius: 进度条圆角半径
#         """
#         # 进度条的整体矩形区域
#         self.rect = pygame.Rect(x, y, width, height)
#         self.width = width
#         self.height = height
#         self.corner_radius = corner_radius

#         # 当前进度值 (0.0 到 1.0)
#         self.progress = 0.0

#         # 动画计时器
#         self.pulse_time = 0.0  # 用于颜色脉动
#         self.sheen_time = 0.0  # 用于光泽扫过

#     def update(self, current_progress_value, dt):
#         """
#         更新进度条的状态。
#         :param current_progress_value: 新的进度值 (0.0 到 1.0)
#         :param dt: 上一帧到当前帧的时间差 (delta time)，用于使动画独立于帧率
#         """
#         # 更新进度，并确保其在0到1之间
#         self.progress = max(0.0, min(1.0, current_progress_value))

#         # 更新动画计时器
#         self.pulse_time += dt * PULSE_SPEED
#         self.sheen_time += dt


#     def draw(self, surface):
#         """
#         在给定的surface上绘制进度条。
#         :param surface: Pygame的Surface对象 (通常是主屏幕 screen)
#         """
#         # 1. 绘制进度条的背景轨道 (圆角矩形)
#         pygame.draw.rect(surface, TRACK_COLOR, self.rect, border_radius=self.corner_radius)

#         # 2. 计算当前填充部分的宽度
#         current_fill_width = int(self.width * self.progress)

#         # 只有当有进度时才绘制填充部分和效果
#         if current_fill_width > 0:
#             # 创建填充部分的矩形区域
#             # 注意：为了正确绘制圆角，填充部分的矩形需要从进度条的左边开始
#             fill_rect_area = pygame.Rect(self.rect.left, self.rect.top, current_fill_width, self.height)

#             # 3. 计算脉动的颜色
#             # 使用正弦函数让颜色亮度在基础色和“基础色+增量色”之间平滑过渡
#             # (1 + sin(time)) / 2 会产生一个在 0 到 1 之间摆动的脉冲因子
#             pulse_factor = (1 + math.sin(self.pulse_time)) / 2.0
            
#             # 根据脉冲因子计算当前填充颜色
#             current_fill_color_r = min(255, FILL_BASE_COLOR[0] + int(FILL_PULSE_ADD_COLOR[0] * pulse_factor))
#             current_fill_color_g = min(255, FILL_BASE_COLOR[1] + int(FILL_PULSE_ADD_COLOR[1] * pulse_factor))
#             current_fill_color_b = min(255, FILL_BASE_COLOR[2] + int(FILL_PULSE_ADD_COLOR[2] * pulse_factor))
#             current_pulsing_fill_color = (current_fill_color_r, current_fill_color_g, current_fill_color_b)

#             # 4. 绘制填充部分
#             # 为了正确显示圆角，特别是当填充部分很窄时，我们需要一些技巧。
#             # Pygame的draw.rect对于非常窄但需要两端都是圆角的矩形处理不完美。
#             # 一个常用的方法是创建一个带alpha通道的surface，在上面绘制，然后blit。
#             # 或者，我们可以直接绘制，当宽度足够时，圆角效果是好的。
#             # 对于宽度小于高度的情况，圆角可能不会完全像预期的那样是半圆形。
            
#             # 创建一个与填充区域大小相同的临时Surface，并使其透明
#             temp_fill_surface = pygame.Surface((current_fill_width, self.height), pygame.SRCALPHA)
#             temp_fill_surface.fill((0,0,0,0)) # 完全透明的背景

#             # 在这个临时Surface上绘制实际的填充颜色（带圆角）
#             # rect的x,y是相对于这个temp_fill_surface的(0,0)
#             pygame.draw.rect(temp_fill_surface, current_pulsing_fill_color, (0, 0, current_fill_width, self.height),
#                              border_radius=self.corner_radius)
            
#             # 将这个临时Surface blit到主屏幕上进度条的正确位置
#             surface.blit(temp_fill_surface, (self.rect.left, self.rect.top))


#             # 5. 绘制光泽扫过效果 (Sheen Effect)
#             # 光泽条的x位置会随时间移动
#             # (self.sheen_time * SHEEN_SPEED) 计算总位移
#             # % (self.width + SHEEN_WIDTH) 使其在进度条总宽度+光泽自身宽度范围内循环
#             # - SHEEN_WIDTH 是为了让光泽从左边完全移出屏幕外开始，到右边完全移出屏幕外结束
#             sheen_x_offset = (self.sheen_time * SHEEN_SPEED) % (self.width + SHEEN_WIDTH * 2) - SHEEN_WIDTH
            
#             # 光泽条的矩形定义 (相对于进度条的左上角)
#             sheen_rect = pygame.Rect(sheen_x_offset, 0, SHEEN_WIDTH, self.height)

#             # 创建一个与填充区域相同大小的临时Surface用于绘制光泽，并进行裁剪
#             sheen_mask_surface = pygame.Surface((current_fill_width, self.height), pygame.SRCALPHA)
#             sheen_mask_surface.fill((0,0,0,0)) # 完全透明

#             # 在这个mask_surface上绘制光泽条。
#             # 注意：sheen_rect的x坐标是相对于整个进度条的，而我们是在一个大小为current_fill_width的surface上绘制
#             # 所以需要调整sheen_rect的x坐标
#             # 只有当sheen_rect与当前填充区域有重叠时才绘制
            
#             # 光泽的实际绘制区域，使用一个带alpha的Surface来创建半透明效果
#             # (如果SHEEN_COLOR本身带alpha，可以直接用)
#             # 我们将光泽绘制在之前创建的 temp_fill_surface 之上，因为它已经有了正确的圆角形状
#             # 但要注意，光泽应该只显示在已填充的进度上。
#             # 最好的方法是：
#             # 1. 创建一个与总进度条相同大小的透明Surface。
#             # 2. 在上面画出当前进度条的圆角填充形状（作为蒙版）。
#             # 3. 在这个Surface上画出移动的光泽条。
#             # 4. Blit这个Surface。
#             #
#             # 简化方法：直接在temp_fill_surface（已填充的进度条部分）上绘制光泽。
#             # 光泽条的x是相对于temp_fill_surface的0点
            
#             # 创建光泽的Surface (可以预先创建以优化)
#             sheen_bar_surface = pygame.Surface(sheen_rect.size, pygame.SRCALPHA)
#             sheen_bar_surface.fill(SHEEN_COLOR) # 用半透明颜色填充

#             # 将光泽条blit到之前绘制了填充颜色的temp_fill_surface上
#             # sheen_x_offset是相对于整个进度条左边缘的
#             # 我们需要相对于temp_fill_surface的左边缘，即 (sheen_x_offset)
#             # 并且只在temp_fill_surface的区域内blit
#             # pygame.Surface.blit() 有一个 area 参数可以用来指定源Surface的某一部分进行blit
#             # 这里，我们直接将完整的sheen_bar_surface blit到temp_fill_surface的(sheen_x_offset, 0)位置
#             # temp_fill_surface 的blit操作会自动处理边界。
            
#             # Blit光泽到主屏幕上，但要确保它被已填充的进度条形状所裁剪
#             # 最简单的方法是使用混合模式 pygame.BLEND_RGBA_ADD
#             # 这里我们创建一个新的surface来组合填充和光泽
            
#             # 我们在之前已经有了temp_fill_surface，它就是当前进度的形状和颜色
#             # 现在在它上面添加光泽
#             # sheen_x_offset_relative_to_fill_start = sheen_x_offset - self.rect.left (这是错误的)
#             # sheen_x_offset is relative to self.rect.left already in its calculation logic
#             # We need to blit the sheen onto the temp_fill_surface (which starts at 0,0 relative to itself)
#             # The sheen_rect's x is `sheen_x_offset`.
            
#             # 绘制光泽 (确保它只在已填充的区域显示)
#             # 先画一个光泽矩形
#             sheen_draw_rect = pygame.Rect(self.rect.left + sheen_x_offset, self.rect.top, SHEEN_WIDTH, self.height)
            
#             # 创建一个裁剪区域，即当前填充的进度条区域
#             clip_area_for_sheen = pygame.Rect(self.rect.left, self.rect.top, current_fill_width, self.height)
            
#             # 保存当前裁剪区
#             original_clip = surface.get_clip()
#             # 设置裁剪区为当前填充进度
#             surface.set_clip(clip_area_for_sheen)
            
#             # 在裁剪区域内绘制光泽
#             # 为了光泽的圆角与进度条一致，我们需要更复杂的方法，或者接受光泽是直角的
#             # 简单起见，光泽是直角的，但只在进度条区域可见
#             pygame.draw.rect(surface, SHEEN_COLOR, sheen_draw_rect) # 使用 surface.set_clip()
#                                                                  # SHEEN_COLOR本身带alpha，可以直接用
            
#             # 恢复裁剪区
#             surface.set_clip(original_clip)


#         # 6. 绘制进度条边框 (在最上层，覆盖所有内容)
#         pygame.draw.rect(surface, BORDER_COLOR, self.rect, width=2, border_radius=self.corner_radius) # width=2 表示边框粗细

#         # 7. 绘制进度百分比文本
#         progress_text_str = f"{int(self.progress * 100)}%"
#         text_surface = progress_font.render(progress_text_str, True, TEXT_COLOR)
#         text_rect = text_surface.get_rect(center=self.rect.center) # 将文本居中于进度条
#         surface.blit(text_surface, text_rect)


# # --- 创建进度条实例 ---
# my_progress_bar = PulsingProgressBar(BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT, CORNER_RADIUS)

# # --- 模拟进度 ---
# # 这个变量将从0增加到1，模拟加载过程
# simulated_progress = 0.0
# progress_increase_speed = 0.05 # 每秒增加5%的进度 (20秒完成100%)

# # --- 主游戏循环 ---
# running = True
# while running:
#     # 计算时间差 (delta time - dt)，使动画与帧率无关
#     dt = clock.tick(FPS) / 1000.0  # dt 是秒为单位的时间

#     # --- 事件处理 ---
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE: # 按ESC退出
#                 running = False
#             if event.key == pygame.K_SPACE: # 按空格键重置进度 (用于演示)
#                 simulated_progress = 0.0
#                 my_progress_bar.pulse_time = 0.0 # 重置动画时间
#                 my_progress_bar.sheen_time = 0.0


#     # --- 更新逻辑 ---
#     # 模拟进度增加
#     if simulated_progress < 1.0:
#         simulated_progress += progress_increase_speed * dt
#     simulated_progress = min(1.0, simulated_progress) # 确保不超过100%

#     # 更新进度条
#     my_progress_bar.update(simulated_progress, dt)

#     # --- 绘制 ---
#     screen.fill(BACKGROUND_COLOR) # 填充背景

#     my_progress_bar.draw(screen)  # 绘制进度条

#     pygame.display.flip()         # 更新整个屏幕显示

# # --- 退出 Pygame ---
# pygame.quit()


# import turtle
# import time
# import random

# # 初始化画布和设置
# screen = turtle.Screen()
# screen.title("Python 加载脉冲 - 动画进度条")
# screen.bgcolor("white")
# screen.setup(width=800, height=300)
# screen.tracer(0)  # 关闭自动刷新，提高性能

# # 创建画笔字典，管理不同元素
# pen_dict = {}

# # 创建进度条背景
# def create_progress_bar_bg():
#     pen = turtle.Turtle()
#     pen.speed(0)
#     pen.hideturtle()
#     pen.penup()
#     pen.goto(-300, 0)
#     pen.pendown()
#     pen.pensize(35)
#     pen.color("lightblue")
#     pen.forward(600)
#     pen_dict["bg"] = pen

# # 创建进度条填充
# def create_progress_bar_fill():
#     pen = turtle.Turtle()
#     pen.speed(0)
#     pen.hideturtle()
#     pen.penup()
#     pen.goto(-300, 0)
#     pen.pendown()
#     pen.pensize(30)
#     pen_dict["fill"] = pen

# # 创建百分比文字
# def create_percentage_text():
#     pen = turtle.Turtle()
#     pen.speed(0)
#     pen.hideturtle()
#     pen.penup()
#     pen.goto(0, 60)
#     pen.color("darkblue")
#     pen_dict["percent"] = pen

# # 创建提示文字
# def create_prompt_text():
#     pen = turtle.Turtle()
#     pen.speed(0)
#     pen.hideturtle()
#     pen.penup()
#     pen.goto(0, -100)
#     pen.color("green")
#     pen_dict["prompt"] = pen

# # 创建装饰星星
# def create_decoration_stars(count=8):
#     stars = []
#     for i in range(count):
#         pen = turtle.Turtle()
#         pen.speed(0)
#         pen.hideturtle()
#         pen.penup()
#         stars.append(pen)
#     pen_dict["stars"] = stars

# # 绘制星星
# def draw_star(pen, size, color):
#     pen.color(color)
#     pen.begin_fill()
#     for _ in range(5):
#         pen.forward(size)
#         pen.right(144)
#     pen.end_fill()

# # 显示加载中的提示
# def show_loading_prompt():
#     pen = pen_dict["prompt"]
#     pen.clear()
#     pen.write("正在加载中...", align="center", font=("Arial", 20, "normal"))

# # 显示加载完成的提示
# def show_complete_prompt():
#     pen = pen_dict["prompt"]
#     pen.clear()
#     pen.write("加载完成！", align="center", font=("Arial", 28, "bold"))

# # 更新百分比显示
# def update_percentage(percent):
#     pen = pen_dict["percent"]
#     pen.clear()
#     pen.write(f"{percent}%", align="center", font=("Arial", 36, "bold"))

# # 更新进度条填充
# def update_progress_bar(percent):
#     fill_pen = pen_dict["fill"]
#     length = (percent / 100) * 600
    
#     # 脉冲颜色效果（HSV颜色空间）
#     hue = (time.time() * 2 % 1)  # 颜色随时间变化
#     r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
#     fill_pen.color(r, g, b)
    
#     fill_pen.penup()
#     fill_pen.goto(-300, 0)
#     fill_pen.pendown()
#     fill_pen.setheading(0)
#     fill_pen.forward(length)

# # 更新星星动画
# def update_stars_animation(percent):
#     stars = pen_dict["stars"]
#     positions = [
#         (-350, 200), (-200, 250), (0, 220), (200, 280),
#         (-350, -200), (-200, -250), (0, -220), (200, -280)
#     ]
    
#     for i, star in enumerate(stars):
#         star.penup()
#         star.goto(positions[i])
        
#         # 星星闪烁效果
#         if percent % 10 < 5:
#             size = 10 + (percent % 5) * 2
#             draw_star(star, size, "gold")
#         else:
#             star.clear()

# # 主函数
# def main():
#     # 创建所有UI元素
#     create_progress_bar_bg()
#     create_progress_bar_fill()
#     create_percentage_text()
#     create_prompt_text()
#     create_decoration_stars()
    
#     show_loading_prompt()
    
#     # 模拟加载过程
#     for i in range(101):
#         update_percentage(i)
#         update_progress_bar(i)
#         update_stars_animation(i)
        
#         screen.update()  # 手动刷新屏幕
#         time.sleep(0.03)  # 控制动画速度
    
#     # 加载完成后的动画效果
#     for _ in range(10):
#         # 闪烁完成提示
#         show_complete_prompt()
#         screen.update()
#         time.sleep(0.2)
        
#         pen_dict["prompt"].clear()
#         screen.update()
#         time.sleep(0.1)
    
#     show_complete_prompt()  # 最终显示完成提示
    
#     # 保持窗口打开
#     screen.mainloop()

# if __name__ == "__main__":
#     # 导入colorsys模块用于颜色处理
#     import colorsys
#     main()    