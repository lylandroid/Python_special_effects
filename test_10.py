import pygame
import numpy as np
import asyncio
import platform
import math
import random

# 初始化 Pygame，设置窗口和字体
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("波浪文字与倒计时时钟")
font = pygame.font.SysFont("arial", 36)  # 使用 Arial 字体，大小 36
clock = pygame.time.Clock()
FPS = 60

# 定义颜色（RGB格式）
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 波浪文字参数
text = "Hello Waves!"  # 要显示的文字
text_chars = list(text)  # 将文字拆分成字符列表
char_surfaces = [font.render(char, True, WHITE) for char in text_chars]  # 渲染每个字符
char_width = char_surfaces[0].get_width()  # 字符宽度
wave_amplitude = 20  # 波浪幅度
wave_frequency = 0.1  # 波浪频率
wave_speed = 0.05  # 波浪移动速度

# 倒计时参数
countdown_seconds = 60  # 倒计时初始秒数
start_time = pygame.time.get_ticks() / 1000  # 记录开始时间（秒）
tick_sound = None  # 滴答音效

# 粒子效果参数
particles = []  # 存储粒子
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)  # 粒子大小
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))  # 随机颜色
        self.speed_y = random.uniform(-2, 2)  # 垂直速度
        self.speed_x = random.uniform(-2, 2)  # 水平速度
        self.life = random.randint(30, 60)  # 粒子存活时间（帧）

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

# 生成滴答音效（使用 NumPy 创建正弦波声音）
def create_tick_sound():
    sample_rate = 44100  # 采样率
    duration = 0.1  # 音效持续时间（秒）
    frequency = 440  # 音效频率（Hz）
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # 生成正弦波
    sound_array = (wave * 32767).astype(np.int16)  # 转换为 16 位音频格式
    sound_array = np.column_stack((sound_array, sound_array))  # 转换为立体声
    return pygame.sndarray.make_sound(sound_array)

# 初始化音效
tick_sound = create_tick_sound()

# 设置函数：初始化游戏环境
def setup():
    pass  # 这里可以添加额外的初始化逻辑

# 更新函数：处理游戏逻辑
def update_loop():
    global particles
    current_time = pygame.time.get_ticks() / 1000  # 当前时间（秒）
    elapsed_time = current_time - start_time  # 已过去的时间
    remaining_time = max(0, countdown_seconds - elapsed_time)  # 剩余时间

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return

    # 绘制渐变背景
    for y in range(HEIGHT):
        color = (0, int(255 * (y / HEIGHT)), int(255 * (1 - y / HEIGHT)))  # 蓝色到绿色渐变
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    # 绘制波浪文字
    for i, char_surface in enumerate(char_surfaces):
        x = 50 + i * char_width  # 字符的 X 位置
        # 使用正弦函数计算 Y 位置，创建波浪效果
        y = HEIGHT // 3 + math.sin(i * wave_frequency + current_time * wave_speed) * wave_amplitude
        screen.blit(char_surface, (x, y))
        # 在字符位置添加粒子
        if random.random() < 0.1:  # 10% 概率生成粒子
            particles.append(Particle(x + char_width / 2, y))

    # 绘制倒计时表盘
    clock_center = (WIDTH - 150, HEIGHT // 2)  # 表盘中心
    clock_radius = 100  # 表盘半径
    pygame.draw.circle(screen, WHITE, clock_center, clock_radius, 5)  # 绘制表盘边框
    # 绘制秒针
    seconds_angle = (remaining_time % 60) * 6  # 每秒旋转 6 度
    seconds_length = clock_radius - 10
    seconds_end = (
        clock_center[0] + seconds_length * math.cos(math.radians(seconds_angle - 90)),
        clock_center[1] + seconds_length * math.sin(math.radians(seconds_angle - 90))
    )
    pygame.draw.line(screen, RED, clock_center, seconds_end, 3)
    # 显示剩余时间
    time_text = font.render(f"{int(remaining_time)}s", True, WHITE)
    screen.blit(time_text, (clock_center[0] - 20, clock_center[1] + clock_radius + 10))

    # 播放滴答音效
    if int(remaining_time * 2) % 2 == 0:  # 每半秒触发一次
        tick_sound.play()

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