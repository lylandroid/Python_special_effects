import pygame
import random
import math

# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置窗口标题
pygame.display.set_caption("爆炸冲击波效果")

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 冲击波类
class Shockwave:
    def __init__(self, x, y):
        self.x = x  # 冲击波中心的 x 坐标
        self.y = y  # 冲击波中心的 y 坐标
        self.radius = 10  # 初始半径
        self.max_radius = 200 # 最大半径
        self.speed = 2  # 扩散速度
        self.width = 15 # 冲击波的宽度
        self.color = (random.randint(100, 255), random.randint(50, 150), random.randint(0, 50)) # 随机颜色

    def update(self):
        # 更新半径，使其随时间变大
        self.radius += self.speed
        # 当冲击波扩散时，其宽度逐渐减小
        if self.width > 0:
            self.width -= 0.1

    def draw(self, surface):
        # 如果冲击波的宽度大于0，则绘制
        if self.width > 0:
            # 使用 pygame.draw.circle() 来绘制一个圆环来模拟冲击波
            # 参数分别是：绘制的表面，颜色，圆心坐标，半径，宽度
            pygame.draw.circle(surface, self.color, (self.x, self.y), int(self.radius), int(self.width))

# 创建一个列表来存储所有的冲击波
shockwaves = []

# 游戏主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        # 如果点击了窗口的关闭按钮，则退出循环
        if event.type == pygame.QUIT:
            running = False
        # 如果按下了鼠标左键，则在鼠标点击的位置创建一个新的冲击波
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # 1 代表鼠标左键
                # 在鼠标点击的位置创建一个新的 Shockwave 对象，并添加到列表中
                shockwaves.append(Shockwave(event.pos[0], event.pos[1]))

    # 更新背景为黑色
    screen.fill(BLACK)

    # 更新和绘制所有的冲击波
    for wave in shockwaves:
        wave.update()
        wave.draw(screen)

    # 移除已经消失的冲击波
    # 创建一个新的列表，只包含那些宽度大于0的冲击波
    shockwaves = [wave for wave in shockwaves if wave.width > 0]

    # 更新屏幕显示
    pygame.display.flip()

    # 控制游戏帧率
    pygame.time.Clock().tick(60)

# 退出 Pygame
pygame.quit()