import pygame
import math
import random

# 初始化 Pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("万花筒之梦 - 少儿编程创意特效")

# 设置颜色和背景
BLACK = (0, 0, 0)
CENTER = (WIDTH // 2, HEIGHT // 2)

# 设置图形对称数量（片段数）
NUM_SYMMETRY = 12

# 用于存储彩色点
particles = []

# 定义颜色函数：根据角度生成彩虹色
def get_rainbow_color(angle):
    r = int(128 + 127 * math.sin(angle))
    g = int(128 + 127 * math.sin(angle + 2 * math.pi / 3))
    b = int(128 + 127 * math.sin(angle + 4 * math.pi / 3))
    return (r, g, b)

# 主循环控制变量
clock = pygame.time.Clock()
running = True
angle_offset = 0

while running:
    clock.tick(60)  # 每秒60帧

    # 检查退出事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充背景为黑色，并带有透明度实现“拖影”效果
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 20))  # 最后的数字是透明度
    screen.blit(overlay, (0, 0))

    # 每一帧添加一个新的彩色点
    angle = random.uniform(0, 2 * math.pi)
    radius = random.uniform(20, 200)
    x = CENTER[0] + math.cos(angle) * radius
    y = CENTER[1] + math.sin(angle) * radius
    color = get_rainbow_color(angle + angle_offset)
    size = random.randint(2, 4)
    particles.append((x, y, color, size))

    # 限制点数量，防止卡顿
    if len(particles) > 300:
        particles.pop(0)

    # 绘制所有点，并以对称方式复制
    for p in particles:
        x0, y0, color, size = p
        dx = x0 - CENTER[0]
        dy = y0 - CENTER[1]
        for i in range(NUM_SYMMETRY):
            theta = 2 * math.pi * i / NUM_SYMMETRY + angle_offset
            rot_x = dx * math.cos(theta) - dy * math.sin(theta)
            rot_y = dx * math.sin(theta) + dy * math.cos(theta)
            draw_x = int(CENTER[0] + rot_x)
            draw_y = int(CENTER[1] + rot_y)
            pygame.draw.circle(screen, color, (draw_x, draw_y), size)

    # 增加角度偏移，让图案旋转
    angle_offset += 0.01

    # 更新屏幕显示
    pygame.display.flip()

# 退出 Pygame
pygame.quit()
