import pygame
import random
import math

# 初始化 pygame
pygame.init()

# 设置窗口尺寸
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("粒子喷泉 - 五彩视觉盛宴")

# 设置时钟，控制帧率
clock = pygame.time.Clock()

# 粒子类定义
class Particle:
    def __init__(self, x, y):
        # 初始位置为中心点
        self.x = x
        self.y = y
        
        # 随机方向（用角度+三角函数控制方向）
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        # 粒子的颜色是随机的
        self.color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )

        # 粒子的生命值
        self.life = 100

    def update(self):
        # 更新位置
        self.x += self.vx
        self.y += self.vy

        # 重力效果
        self.vy += 0.05  # 模拟向下的加速度

        # 生命值减少
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            radius = max(1, self.life // 10)  # 根据生命值动态调整大小
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), radius)

# 粒子容器
particles = []

# 主循环
running = True
while running:
    screen.fill((0, 0, 0))  # 黑色背景

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 每一帧添加新粒子
    for _ in range(10):  # 每帧发射 10 个粒子
        particle = Particle(WIDTH // 2, HEIGHT // 2)
        particles.append(particle)

    # 更新和绘制粒子
    for particle in particles[:]:  # 遍历粒子列表
        particle.update()
        particle.draw(screen)

        # 如果生命结束，则从列表中移除
        if particle.life <= 0:
            particles.remove(particle)

    # 刷新屏幕
    pygame.display.flip()
    clock.tick(60)  # 每秒 60 帧

# 退出 pygame
pygame.quit()
