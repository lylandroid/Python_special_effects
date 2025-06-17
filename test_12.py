import pygame
import math
import sys
# 初始化 Pygame
pygame.init()

# 设置窗口大小和标题
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("旋转之星 - 发光动画")

# 设置颜色和字体
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 设置时钟控制帧率
clock = pygame.time.Clock()

# 生成五角星顶点的函数
def create_star_points(center, outer_radius, inner_radius, points=5, angle_offset=0):
    """生成五角星的顶点坐标"""
    star_points = []
    angle = math.pi / points  # 每个角之间的弧度
    for i in range(points * 2):
        radius = outer_radius if i % 2 == 0 else inner_radius
        theta = i * angle + angle_offset
        x = center[0] + math.cos(theta) * radius
        y = center[1] + math.sin(theta) * radius
        star_points.append((x, y))
    return star_points

# 渲染发光星星函数
def draw_glowing_star(surface, center, outer_r, inner_r, angle, color):
    # 绘制多个透明星星，模拟发光效果（从大到小）
    for i in range(5, 0, -1):
        alpha = int(30 * i)  # 透明度逐渐增强
        size_multiplier = 1 + i * 0.1
        glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        glow_color = (*color, alpha)
        points = create_star_points(center, outer_r * size_multiplier, inner_r * size_multiplier, angle_offset=angle)
        pygame.draw.polygon(glow_surface, glow_color, points)
        surface.blit(glow_surface, (0, 0))

    # 画最亮的星星（不透明）
    points = create_star_points(center, outer_r, inner_r, angle_offset=angle)
    pygame.draw.polygon(surface, color, points)

# 主循环变量
angle = 0  # 初始旋转角度

# 主动画循环
running = True
while running:
    clock.tick(60)  # 每秒60帧
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 清屏
    screen.fill(BLACK)

    # 每帧增加一点旋转角度（逆时针）
    angle += 0.02

    # 发光颜色动态变化（用 HSV 渐变）
    hue = (pygame.time.get_ticks() % 3600) / 3600
    import colorsys
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    color = (int(r * 255), int(g * 255), int(b * 255))

    # 绘制发光旋转星星
    draw_glowing_star(screen, (WIDTH // 2, HEIGHT // 2), 60, 25, angle, color)

    # 更新画面
    pygame.display.flip()

# 退出
pygame.quit()
sys.exit()
