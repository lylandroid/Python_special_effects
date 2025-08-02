import pygame
import math
import random
import asyncio
import platform

# 初始化Pygame，准备绘图环境
try:
    pygame.init()
except Exception as e:
    print(f"Pygame初始化失败: {e}")
    import sys
    sys.exit(1)

# 设置窗口大小
WIDTH, HEIGHT = 800, 600
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("声波视觉特效")
except Exception as e:
    print(f"窗口创建失败: {e}")
    import sys
    sys.exit(1)

# 定义颜色（RGB格式）
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (255, 50, 50),   # 红色
    (50, 255, 50),   # 绿色
    (50, 50, 255),   # 蓝色
    (255, 255, 50)   # 黄色
]

# 声波类，用于管理波形属性和行为
class SoundWave:
    def __init__(self, frequency, amplitude, offset_y, color):
        self.frequency = frequency    # 波形频率（控制波的密集程度）
        self.amplitude = amplitude    # 波形振幅（控制波的高度）
        self.offset_y = offset_y      # 波形垂直偏移（屏幕Y坐标）
        self.color = color            # 波形颜色
        self.phase = 0                # 相位，用于动画效果

    def update(self, time):
        # 更新相位，控制波形动态移动
        self.phase += 0.1
        # 随机调整振幅，模拟音频强度的变化
        self.amplitude = max(20, self.amplitude + random.uniform(-5, 5))

    def draw(self, surface):
        # 创建波形点列表
        points = []
        for x in range(WIDTH):
            # 使用正弦函数生成波形，模拟音频波动
            y = self.offset_y + self.amplitude * math.sin(
                2 * math.pi * self.frequency * x / WIDTH + self.phase
            )
            points.append((x, int(y)))
        # 绘制波形线条
        pygame.draw.lines(surface, self.color, False, points, 2)

# 存储所有声波的列表
waves = []

# 帧率设置
FPS = 60
clock = pygame.time.Clock()

def setup():
    # 清空声波列表
    waves.clear()
    # 初始化三条声波，分别位于屏幕不同高度
    for i in range(3):
        waves.append(SoundWave(
            frequency=2 + i * 0.5,           # 不同频率
            amplitude=50 + i * 20,           # 不同振幅
            offset_y=HEIGHT // 4 * (i + 1),  # 不同垂直位置
            color=random.choice(COLORS)      # 随机颜色
        ))
    # 设置背景颜色为黑色
    screen.fill(BLACK)

def update_loop(time):
    try:
        # 处理事件（例如关闭窗口或鼠标点击）
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标点击添加新声波
                x, y = pygame.mouse.get_pos()
                waves.append(SoundWave(
                    frequency=random.uniform(1, 3),
                    amplitude=random.randint(30, 80),
                    offset_y=y,
                    color=random.choice(COLORS)
                ))

        # 清空屏幕
        screen.fill(BLACK)

        # 更新并绘制所有声波
        for wave in waves:
            wave.update(time)
            wave.draw(screen)

        # 更新屏幕显示
        pygame.display.flip()
        return True
    except Exception as e:
        print(f"渲染失败: {e}")
        return False

async def main():
    setup()  # 初始化环境
    time = 0
    running = True
    while running:
        running = update_loop(time)
        time += 0.1  # 控制动画速度
        clock.tick(FPS)  # 控制帧率
        await asyncio.sleep(1.0 / FPS)  # 异步等待，适配Pyodide

# 适配Pyodide环境
if platform.system() == "Emscripten":
    try:
        asyncio.ensure_future(main())
    except Exception as e:
        print(f"异步循环启动失败: {e}")
else:
    if __name__ == "__main__":
        try:
            asyncio.run(main())
        except Exception as e:
            print(f"主循环运行失败: {e}")