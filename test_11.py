import pygame
import random
import math
import asyncio
import platform

# 初始化 Pygame，设置窗口
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("弹跳小球特效")
clock = pygame.time.Clock()
FPS = 60

# 定义颜色（RGB格式）
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 小球参数
ball = {
    'x': WIDTH // 2,  # 小球初始 X 坐标（屏幕中心）
    'y': HEIGHT // 2,  # 小球初始 Y 坐标
    'radius': 20,  # 小球半径
    'speed_x': 5,  # X 轴速度（像素/帧）
    'speed_y': 5,  # Y 轴速度
    'color': RED  # 初始颜色
}

# 尾迹效果参数
trail_positions = []  # 存储小球历史位置
trail_length = 20  # 尾迹长度
trail_fade = 0.8  # 尾迹透明度衰减因子

# 粒子效果参数
particles = []  # 存储粒子
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)  # 粒子大小
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))  # 随机颜色
        self.speed_x = random.uniform(-3, 3)  # 随机水平速度
        self.speed_y = random.uniform(-3, 3)  # 随机垂直速度
        self.life = random.randint(20, 40)  # 粒子存活时间（帧）

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

# 设置函数：初始化游戏环境
def setup():
    pass  # 这里可以添加额外的初始化逻辑

# 更新函数：处理游戏逻辑
def update_loop():
    global trail_positions, particles

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return

    # 更新小球位置
    ball['x'] += ball['speed_x']
    ball['y'] += ball['speed_y']

    # 边界碰撞检测
    collision = False
    if ball['x'] - ball['radius'] <= 0 or ball['x'] + ball['radius'] >= WIDTH:
        ball['speed_x'] = -ball['speed_x']  # 反转 X 速度
        ball['x'] = max(ball['radius'], min(WIDTH - ball['radius'], ball['x']))  # 防止越界
        collision = True
    if ball['y'] - ball['radius'] <= 0 or ball['y'] + ball['radius'] >= HEIGHT:
        ball['speed_y'] = -ball['speed_y']  # 反转 Y 速度
        ball['y'] = max(ball['radius'], min(HEIGHT - ball['radius'], ball['y']))  # 防止越界
        collision = True

    # 碰撞时生成粒子
    if collision:
        for _ in range(10):  # 生成 10 个粒子
            particles.append(Particle(ball['x'], ball['y']))

    # 更新尾迹
    trail_positions.append((ball['x'], ball['y']))
    if len(trail_positions) > trail_length:
        trail_positions.pop(0)  # 移除最旧的位置

    # 动态改变小球颜色（基于位置）
    ball['color'] = (
        int(255 * (ball['x'] / WIDTH)),  # 红色随 X 变化
        int(255 * (ball['y'] / HEIGHT)),  # 绿色随 Y 变化
        255  # 蓝色固定
    )

    # 绘制渐变背景
    for y in range(HEIGHT):
        color = (int(255 * (y / HEIGHT)), 0, int(255 * (1 - y / HEIGHT)))  # 红色到蓝色渐变
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    # 绘制尾迹
    for i, pos in enumerate(trail_positions):
        alpha = int(255 * (trail_fade ** (trail_length - i)))  # 计算透明度
        trail_surface = pygame.Surface((ball['radius'] * 2, ball['radius'] * 2), pygame.SRCALPHA)
        pygame.draw.circle(trail_surface, (*ball['color'], alpha), (ball['radius'], ball['radius']), ball['radius'])
        screen.blit(trail_surface, (pos[0] - ball['radius'], pos[1] - ball['radius']))

    # 绘制光晕效果
    glow_surface = pygame.Surface((ball['radius'] * 4, ball['radius'] * 4), pygame.SRCALPHA)
    for i in range(10, 0, -1):
        glow_alpha = int(50 / i)  # 光晕透明度
        pygame.draw.circle(glow_surface, (*ball['color'], glow_alpha), (ball['radius'] * 2, ball['radius'] * 2), ball['radius'] + i * 2)
    screen.blit(glow_surface, (ball['x'] - ball['radius'] * 2, ball['y'] - ball['radius'] * 2))

    # 绘制小球
    pygame.draw.circle(screen, ball['color'], (int(ball['x']), int(ball['y'])), ball['radius'])

    # 更新和绘制粒子
    particles = [p for p in particles if p.life > 0]  # 移除死亡粒子
    for particle in particles:
        particle.update()
        particle.draw(screen)

    # 更新屏幕
    pygame.display.flip()

# 主循环，适配 Pyodide
async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())