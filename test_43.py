import pygame
import random
import math
import asyncio
import platform

# 初始化Pygame
pygame.init()

# 设置屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("烟雾弥漫动画")

# 定义颜色
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# 定义粒子类，用于管理每个烟雾粒子
class SmokeParticle:
    def __init__(self):
        """初始化一个烟雾粒子"""
        self.x = SCREEN_WIDTH // 2  # 从屏幕中心开始
        self.y = SCREEN_HEIGHT // 2
        self.radius = random.randint(5, 15)  # 随机半径
        self.color = random.choice(COLORS)  # 随机颜色
        self.angle = random.uniform(0, 2 * math.pi)  # 随机初始角度
        self.speed = random.uniform(1, 3)  # 随机扩散速度
        self.angular_speed = random.uniform(-0.05, 0.05)  # 随机旋转速度
        self.life = 100  # 粒子生命周期（帧数）
        self.alpha = 255  # 初始透明度

    def update(self):
        """更新粒子的位置、角度和透明度"""
        # 使用正弦和余弦函数计算螺旋轨迹
        self.angle += self.angular_speed
        radius = self.speed * (100 - self.life)  # 半径随时间增加
        self.x = SCREEN_WIDTH // 2 + radius * math.cos(self.angle)
        self.y = SCREEN_HEIGHT // 2 + radius * math.sin(self.angle)
        
        # 减少生命周期和透明度，模拟消散
        self.life -= 1
        self.alpha = max(0, int(255 * self.life / 100))  # 透明度随生命周期线性减少

    def draw(self, surface):
        """在屏幕上绘制粒子（支持透明度）"""
        # 创建一个临时的表面以支持透明度
        temp_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        # 绘制圆形粒子
        pygame.draw.circle(temp_surface, self.color + (self.alpha,), (self.radius, self.radius), self.radius)
        # 将临时表面绘制到主屏幕
        surface.blit(temp_surface, (int(self.x - self.radius), int(self.y - self.radius)))

# 全局变量
particles = []  # 存储所有烟雾粒子
FPS = 60  # 帧率
clock = pygame.time.Clock()

def setup():
    """初始化游戏设置"""
    screen.fill(BLACK)

async def update_loop():
    """主更新循环，处理粒子生成、更新和绘制"""
    running = True
    while running:
        # 处理退出事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 每帧生成新粒子（控制生成速度）
        if random.random() < 0.1:
            particles.append(SmokeParticle())
        
        # 更新所有粒子
        for particle in particles[:]:  # 使用切片避免修改列表时的错误
            particle.update()
            # 如果粒子生命周期结束，移除它
            if particle.life <= 0:
                particles.remove(particle)
        
        # 绘制背景和所有粒子
        screen.fill(BLACK)
        for particle in particles:
            particle.draw(screen)
        
        # 更新显示
        pygame.display.flip()
        
        # 控制帧率
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

# 主程序，适配Pyodide环境
if platform.system() == "Emscripten":
    setup()
    asyncio.ensure_future(update_loop())
else:
    if __name__ == "__main__":
        setup()
        asyncio.run(update_loop())