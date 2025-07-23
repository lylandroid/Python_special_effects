import pygame
import random
import asyncio
import platform

# 初始化Pygame，准备绘图环境
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("隐身装置特效")

# 定义颜色（RGB格式）
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
BLACK = (0, 0, 0)



# 隐身物体类，用于管理物体的属性和淡入淡出效果
class InvisibilityObject:
    def __init__(self, x, y, radius):
        # 物体中心坐标
        self.x = x
        self.y = y
        # 物体半径
        self.radius = radius
        # 物体透明度（0完全透明，255完全不透明）
        self.alpha = 255
        # 淡入淡出速度（正值表示淡出，负值表示淡入）
        self.alpha_speed = -5
        # 物体颜色
        self.color = BLUE

    def new_color(self):
        return (random.randint(0,255), random.randint(0,255), random.randint(0,255), self.alpha)

    def update(self):
        # 更新透明度
        self.alpha += self.alpha_speed
        # 当透明度达到0（完全透明）或255（完全不透明）时，切换淡入/淡出方向
        if self.alpha <= 0:
            self.alpha = 0
            self.alpha_speed = 5  # 开始淡出
        elif self.alpha >= 255:
            self.alpha = 255
            self.alpha_speed = -5  # 开始淡入
        # 随机移动物体位置，增加动态效果
        self.x += random.uniform(-2, 2)
        self.y += random.uniform(-2, 2)
        # 确保物体不移出屏幕
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self, surface):
        # 创建临时表面以支持透明度
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # 绘制圆形物体
        pygame.draw.circle(temp_surface, self.new_color(), (int(self.x), int(self.y)), self.radius)
        # 将临时表面绘制到主屏幕
        surface.blit(temp_surface, (0, 0))

# 存储所有隐身物体的列表
objects = []

# 帧率设置
FPS = 60
clock = pygame.time.Clock()

def setup():
    # 清空物体列表
    objects.clear()
    # 初始化一个隐身物体
    objects.append(InvisibilityObject(WIDTH // 2, HEIGHT // 2, 50))
    # 设置背景颜色为黑色
    screen.fill(BLACK)

def update_loop():
    # 处理事件（例如关闭窗口或鼠标点击）
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 鼠标点击时在点击位置生成一个新的隐身物体
            x, y = pygame.mouse.get_pos()
            radius = random.randint(30, 70)  # 随机半径
            objects.append(InvisibilityObject(x, y, radius))

    # 清空屏幕
    screen.fill(BLACK)

    # 更新并绘制所有隐身物体
    for obj in objects:
        obj.update()
        obj.draw(screen)

    # 更新屏幕显示
    pygame.display.flip()

async def main():
    setup()  # 初始化游戏环境
    while True:
        update_loop()  # 更新动画
        clock.tick(FPS)  # 控制帧率
        await asyncio.sleep(1.0 / FPS)  # 异步等待，适配Pyodide

# 适配Pyodide环境
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())