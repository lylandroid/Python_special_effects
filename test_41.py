import pygame
import random
import asyncio
import platform

# 初始化Pygame
pygame.init()

# 设置屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("重力坠落动画")

# 定义颜色
WHITE = (255, 255, 255)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# 定义物体类，用于管理每个坠落物体
class FallingObject:
    def __init__(self):
        """初始化一个坠落物体"""
        self.x = random.randint(0, SCREEN_WIDTH)  # 随机x坐标
        self.y = 0  # 从屏幕顶部开始
        self.radius = random.randint(10, 20)  # 随机半径
        self.color = random.choice(COLORS)  # 随机颜色
        self.vy = 0  # 初始垂直速度
        self.gravity = 0.5  # 重力加速度
        self.bounce_factor = 0.7  # 弹跳系数（能量损失）

    def update(self):
        """更新物体的位置和速度"""
        # 应用重力：速度增加
        self.vy += self.gravity
        # 更新y坐标
        self.y += self.vy
        
        # 检测触底并弹跳
        if self.y + self.radius > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.radius  # 保持在底部
            self.vy = -self.vy * self.bounce_factor  # 反向速度并减小（模拟能量损失）

    def draw(self, surface):
        """在屏幕上绘制物体"""
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

# 全局变量
objects = []  # 存储所有坠落物体
FPS = 60  # 帧率
clock = pygame.time.Clock()

def setup():
    """初始化游戏设置"""
    # 清空物体列表
    global objects
    objects = []
    # 设置白色背景
    screen.fill(WHITE)

async def update_loop():
    """主更新循环，处理物体生成、更新和绘制"""
    running = True
    while running:
        # 处理退出事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 每隔几帧随机生成新物体（控制生成速度）
        if random.random() < 0.05:
            objects.append(FallingObject())
        
        # 更新所有物体
        for obj in objects[:]:  # 使用切片避免修改列表时的错误
            obj.update()
            # 如果物体静止（速度很小且在底部），移除它
            if obj.y + obj.radius >= SCREEN_HEIGHT and abs(obj.vy) < 0.1:
                objects.remove(obj)
        
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