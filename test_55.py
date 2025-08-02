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
    pygame.display.set_caption("AI艺术生成特效")
except Exception as e:
    print(f"窗口创建失败: {e}")
    import sys
    sys.exit(1)

# 定义颜色（RGB格式）
BLACK = (0, 0, 0)
COLORS = [
    (255, 50, 50),   # 红色
    (50, 255, 50),   # 绿色
    (50, 50, 255),   # 蓝色
    (255, 255, 50),  # 黄色
    (255, 50, 255)   # 紫色
]

# 艺术图案类，模拟AI生成的抽象效果
class ArtPattern:
    def __init__(self, x, y, size, speed):
        self.x = x              # 图案中心X坐标
        self.y = y              # 图案中心Y坐标
        self.size = size        # 图案大小
        self.speed = speed      # 动画速度
        self.phase = random.uniform(0, 2 * math.pi)  # 随机相位
        self.color = random.choice(COLORS)           # 随机颜色
        self.shape_type = random.choice(['circle', 'square', 'wave'])  # 随机形状

    def update(self, time):
        # 更新相位，控制动画效果
        self.phase += self.speed
        # 随机调整大小，模拟动态变化
        self.size = max(10, self.size + random.uniform(-5, 5))
        # 轻微移动中心点，增加流动性
        self.x += random.uniform(-2, 2)
        self.y += random.uniform(-2, 2)
        # 确保图案不移出屏幕
        self.x = max(self.size, min(WIDTH - self.size, self.x))
        self.y = max(self.size, min(HEIGHT - self.size, self.y))

    def draw(self, surface):
        # 创建临时表面支持透明度
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # 计算动态透明度，模拟AI艺术的渐变效果
        alpha = int(255 * (0.5 + 0.5 * math.sin(self.phase)))
        color = self.color + (alpha,)

        if self.shape_type == 'circle':
            # 绘制圆形图案
            pygame.draw.circle(temp_surface, color, (int(self.x), int(self.y)), int(self.size))
        elif self.shape_type == 'square':
            # 绘制方形图案
            rect = pygame.Rect(int(self.x - self.size), int(self.y - self.size), int(self.size * 2), int(self.size * 2))
            pygame.draw.rect(temp_surface, color, rect, 2)
        elif self.shape_type == 'wave':
            # 绘制波形线条
            points = []
            for x in range(int(self.x - self.size), int(self.x + self.size), 5):
                y = self.y + self.size * math.sin(0.1 * x + self.phase)
                points.append((x, int(y)))
            pygame.draw.lines(temp_surface, color, False, points, 3)

        # 将临时表面绘制到主屏幕
        surface.blit(temp_surface, (0, 0))

# 存储所有艺术图案的列表
patterns = []

# 帧率设置
FPS = 60
clock = pygame.time.Clock()

def setup():
    # 清空图案列表
    patterns.clear()
    # 初始化5个随机图案
    for _ in range(5):
        patterns.append(ArtPattern(
            x=random.randint(100, WIDTH - 100),
            y=random.randint(100, HEIGHT - 100),
            size=random.randint(30, 80),
            speed=random.uniform(0.05, 0.15)
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
                # 鼠标点击添加新图案
                x, y = pygame.mouse.get_pos()
                patterns.append(ArtPattern(
                    x=x,
                    y=y,
                    size=random.randint(20, 60),
                    speed=random.uniform(0.05, 0.2)
                ))

        # 清空屏幕
        screen.fill(BLACK)

        # 更新并绘制所有图案
        for pattern in patterns:
            pattern.update(time)
            pattern.draw(screen)

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