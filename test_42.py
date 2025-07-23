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
pygame.display.set_caption("弹跳狂欢动画")

# 定义颜色
WHITE = (255, 255, 255)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# 定义弹跳物体类
class BouncingObject:
    def __init__(self):
        """初始化一个弹跳物体"""
        self.x = random.randint(50, SCREEN_WIDTH - 50)  # 随机x坐标
        self.y = random.randint(50, SCREEN_HEIGHT - 50)  # 随机y坐标
        self.radius = random.randint(15, 30)  # 随机半径
        self.color = random.choice(COLORS)  # 随机颜色
        self.vx = random.uniform(-5, 5)  # 随机x方向速度
        self.vy = random.uniform(-5, 5)  # 随机y方向速度
        self.mass = self.radius  # 质量与半径成正比（简化计算）

    def update(self):
        """更新物体的位置"""
        self.x += self.vx
        self.y += self.vy
        
        # 检测与屏幕边界的碰撞
        if self.x - self.radius < 0 or self.x + self.radius > SCREEN_WIDTH:
            self.vx = -self.vx  # 反转x方向速度
            self.x = max(self.radius, min(self.x, SCREEN_WIDTH - self.radius))  # 防止越界
        if self.y - self.radius < 0 or self.y + self.radius > SCREEN_HEIGHT:
            self.vy = -self.vy  # 反转y方向速度
            self.y = max(self.radius, min(self.y, SCREEN_HEIGHT - self.radius))  # 防止越界

    def draw(self, surface):
        """在屏幕上绘制物体"""
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def collide(self, other):
        """处理与另一个物体的弹性碰撞"""
        # 计算两物体中心之间的距离
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # 检查是否发生碰撞（距离小于两半径之和）
        if distance < self.radius + other.radius and distance > 0:
            # 计算碰撞后的速度（基于一维弹性碰撞公式，沿连线方向）
            m1, m2 = self.mass, other.mass
            v1, v2 = self.vx, other.vx
            self.vx = (m1 - m2) / (m1 + m2) * v1 + 2 * m2 / (m1 + m2) * v2
            other.vx = 2 * m1 / (m1 + m2) * v1 + (m2 - m1) / (m1 + m2) * v2
            
            v1, v2 = self.vy, other.vy
            self.vy = (m1 - m2) / (m1 + m2) * v1 + 2 * m2 / (m1 + m2) * v2
            other.vy = 2 * m1 / (m1 + m2) * v1 + (m2 - m1) / (m1 + m2) * v2
            
            # 防止物体重叠：稍微调整位置
            overlap = (self.radius + other.radius - distance) / 2
            angle = math.atan2(dy, dx)
            self.x -= overlap * math.cos(angle)
            self.y -= overlap * math.sin(angle)
            other.x += overlap * math.cos(angle)
            other.y += overlap * math.sin(angle)

# 全局变量
objects = [BouncingObject() for _ in range(10)]  # 创建10个弹跳物体
FPS = 60  # 帧率
clock = pygame.time.Clock()

def setup():
    """初始化游戏设置"""
    screen.fill(WHITE)

async def update_loop():
    """主更新循环，处理物体移动、碰撞和绘制"""
    running = True
    while running:
        # 处理退出事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 更新所有物体位置
        for obj in objects:
            obj.update()
        
        # 检查所有物体对之间的碰撞
        for i, obj1 in enumerate(objects):
            for obj2 in objects[i+1:]:
                obj1.collide(obj2)
        
        # 绘制背景和所有物体
        screen.fill(WHITE)
        for obj in objects:
            obj.draw(screen)
        
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