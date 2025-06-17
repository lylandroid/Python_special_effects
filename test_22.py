import pygame
import random
import math
import asyncio
import platform
from PIL import Image, ImageFilter
import io
import numpy as np

# 初始化 Pygame，设置窗口
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("梦幻模糊图像特效")
clock = pygame.time.Clock()
FPS = 60

# 定义颜色（RGB格式）
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 182, 193)

# 粒子参数
particles = []  # 存储粒子
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)  # 粒子大小
        self.color = (random.randint(200, 255), random.randint(150, 200), random.randint(200, 255))  # 粉紫色调
        self.speed_x = random.uniform(-0.5, 0.5)  # 随机水平速度
        self.speed_y = random.uniform(-0.5, 0.5)  # 随机垂直速度
        self.life = random.randint(30, 60)  # 粒子存活时间（帧）

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            alpha = int(255 * (self.life / 60))  # 透明度随生命值减少
            particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*self.color, alpha), (self.size, self.size), self.size)
            surface.blit(particle_surface, (int(self.x) - self.size, int(self.y) - self.size))

# 生成示例图像（由于 Pyodide 不支持本地文件）
def create_sample_image():
    # 创建一个 400x400 的图像，中间画一个彩色渐变圆
    image = Image.new('RGB', (400, 400), (255, 255, 255))
    pixels = image.load()
    center = (200, 200)
    radius = 150
    for x in range(400):
        for y in range(400):
            distance = math.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
            if distance < radius:
                # 彩色渐变圆（粉紫色调）
                color_value = distance / radius
                pixels[x, y] = (
                    int(255 * (1 - color_value)),
                    int(150 + 105 * color_value),
                    int(200 + 55 * (1 - color_value))
                )
    return image

# 处理图像：应用高斯模糊
def process_image():
    # 生成或加载图像
    image = create_sample_image()  # 替换为 Image.open("your_image.jpg") 在非 Pyodide 环境中
    # 调整图像大小以适应窗口
    image = image.resize((WIDTH // 2, HEIGHT // 2), Image.Resampling.LANCZOS)
    # 应用高斯模糊
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=5))  # 模糊半径为5
    # 确保图像为 RGB 格式以兼容 Pygame
    blurred_image_rgb = blurred_image.convert('RGB')
    return blurred_image_rgb

# 将 PIL 图像转换为 Pygame 表面
def pil_to_pygame(pil_image):
    # 确保图像是 RGB 格式
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')
    size = pil_image.size
    data = pil_image.tobytes()
    return pygame.image.fromstring(data, size, 'RGB')

# 设置函数：初始化游戏环境
def setup():
    global blurred_surface
    # 处理图像
    blurred_image = process_image()
    # 转换为 Pygame 表面
    blurred_surface = pil_to_pygame(blurred_image)

# 更新函数：处理游戏逻辑
def update_loop():
    global particles
    current_time = pygame.time.get_ticks() / 1000  # 当前时间（秒）

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return

    # 绘制渐变背景（粉紫色调）
    for y in range(HEIGHT):
        t = (current_time + y / HEIGHT) % 60  # 使用时间和 Y 坐标创建动态效果
        color = (
            int(100 + 50 * math.sin(t * 0.1)),  # 红色渐变
            int(50 + 50 * math.cos(t * 0.1)),   # 绿色渐变
            int(150 + 50 * math.sin(t * 0.05))  # 蓝色渐变
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    # 绘制模糊图像
    screen.blit(blurred_surface, (WIDTH // 4, HEIGHT // 4))

    # 绘制动态光晕（中心脉动）
    glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    glow_radius = 100 + 20 * math.sin(current_time)  # 光晕半径随时间变化
    glow_alpha = int(100 + 50 * math.cos(current_time))  # 光晕透明度脉动
    pygame.draw.circle(glow_surface, (255, 182, 193, glow_alpha), (WIDTH // 2, HEIGHT // 2), int(glow_radius))
    screen.blit(glow_surface, (0, 0))

    # 生成粒子
    if random.random() < 0.2:  # 20% 概率生成粒子
        for _ in range(3):  # 每次生成3个粒子
            x = random.randint(WIDTH // 4, WIDTH * 3 // 4)
            y = random.randint(HEIGHT // 4, HEIGHT * 3 // 4)
            particles.append(Particle(x, y))

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