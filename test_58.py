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
    pygame.display.set_caption("触摸投影特效")
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

# 投影波纹类，模拟触摸点产生的扩散效果
class TouchRipple:
    def __init__(self, x, y, max_radius, speed):
        self.x = x              # 波纹中心X坐标
        self.y = y              # 波纹中心Y坐标
        self.radius = 0         # 当前半径
        self.max_radius = max_radius  # 最大半径
        self.speed = speed      # 扩散速度
        self.color = random.choice(COLORS)  # 随机颜色
        self.alpha = 255        # 初始透明度（0-255）

    def update(self):
        # 增加半径，模拟波纹扩散
        self.radius += self.speed
        # 透明度随半径增加而降低，模拟消散
        self.alpha = max(0, int(255 * (1 - self.radius / self.max_radius)))

    def draw(self, surface):
        # 创建临时表面支持透明度
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # 绘制波纹圆环
        pygame.draw.circle(temp_surface, self.color + (self.alpha,), 
                          (int(self.x), int(self.y)), int(self.radius), 3)
        # 将临时表面叠加到主屏幕
        surface.blit(temp_surface, (0, 0))

# 粒子类，模拟触摸点产生的粒子效果
class TouchParticle:
    def __init__(self, x, y, speed, angle):
        self.x = x              # 粒子初始X坐标
        self.y = y              # 粒子初始Y坐标
        self.speed = speed      # 粒子移动速度
        self.angle = angle      # 粒子移动方向（弧度）
        self.color = random.choice(COLORS)  # 随机颜色
        self.alpha = 255        # 初始透明度
        self.life = 60          # 粒子生命周期（帧数）

    def update(self):
        # 更新粒子位置
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        # 减少生命周期和透明度
        self.life -= 1
        self.alpha = max(0, int(255 * (self.life / 60)))

    def draw(self, surface):
        # 创建临时表面支持透明度
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # 绘制粒子
        pygame.draw.circle(temp_surface, self.color + (self.alpha,), 
                          (int(self.x), int(self.y)), 5)
        # 将临时表面叠加到主屏幕
        surface.blit(temp_surface, (0, 0))

# 存储波纹和粒子的列表
ripples = []
particles = []

# 帧率设置
FPS = 60
clock = pygame.time.Clock()

def setup():
    # 清空波纹和粒子列表
    ripples.clear()
    particles.clear()
    # 设置背景颜色为黑色
    screen.fill(BLACK)

def update_loop():
    try:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN or \
               (event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]):
                # 鼠标点击或拖动生成波纹和粒子
                x, y = pygame.mouse.get_pos()
                ripples.append(TouchRipple(
                    x=x,
                    y=y,
                    max_radius=random.randint(50, 150),
                    speed=random.uniform(1, 3)
                ))
                # 生成5个粒子，随机方向
                for _ in range(5):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(2, 5)
                    particles.append(TouchParticle(x, y, speed, angle))

        # 清空屏幕
        screen.fill(BLACK)

        # 更新并绘制波纹
        for ripple in ripples[:]:
            ripple.update()
            ripple.draw(screen)
            # 移除达到最大半径的波纹
            if ripple.radius >= ripple.max_radius:
                ripples.remove(ripple)

        # 更新并绘制粒子
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            # 移除生命周期结束的粒子
            if particle.life <= 0:
                particles.remove(particle)

        # 更新屏幕
        pygame.display.flip()
        return True
    except Exception as e:
        print(f"渲染失败: {e}")
        return False

async def main():
    setup()  # 初始化环境
    running = True
    while running:
        running = update_loop()
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