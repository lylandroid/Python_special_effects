import pygame
import random
import asyncio
import platform

# 初始化 Pygame
pygame.init()

# 设置窗口大小
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("闪电一击 - 随机锯齿状闪电")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 150, 255)  # 闪电的蓝色光芒
GLOW = (150, 200, 255)  # 闪电边缘的光晕

# 帧率控制
FPS = 30
clock = pygame.time.Clock()

# 闪电路径存储
lightning_path = []

def generate_lightning(start_x, start_y, end_y):
    """生成随机锯齿状闪电路径"""
    path = [(start_x, start_y)]  # 起点
    current_y = start_y
    while current_y < end_y:
        # 随机偏移 x 坐标，制造锯齿效果
        next_x = path[-1][0] + random.randint(-50, 50)
        # 确保 x 坐标不超出屏幕
        next_x = max(50, min(WIDTH - 50, next_x))
        # 每次向下移动一段距离
        current_y += random.randint(20, 50)
        path.append((next_x, current_y))
    return path

def draw_lightning(surface, path):
    """绘制闪电效果，包括主闪电和光晕"""
    if not path:
        return
    # 绘制光晕（较粗的线条）
    for i in range(len(path) - 1):
        pygame.draw.line(surface, GLOW, path[i], path[i + 1], 10)
    # 绘制主闪电（细线条）
    for i in range(len(path) - 1):
        pygame.draw.line(surface, BLUE, path[i], path[i + 1], 3)

def setup():
    """初始化游戏设置"""
    global lightning_path
    screen.fill(BLACK)  # 清空屏幕为黑色背景
    # 随机生成闪电起点 x 坐标
    start_x = random.randint(100, WIDTH - 100)
    lightning_path = generate_lightning(start_x, 50, HEIGHT - 50)

def update_loop():
    """更新游戏状态"""
    global lightning_path
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
    # 每 10 帧重新生成闪电，制造闪烁效果
    if pygame.time.get_ticks() % 10 == 0:
        start_x = random.randint(100, WIDTH - 100)
        lightning_path = generate_lightning(start_x, 50, HEIGHT - 50)
    
    # 清空屏幕
    screen.fill(BLACK)
    # 绘制闪电
    draw_lightning(screen, lightning_path)
    # 更新显示
    pygame.display.flip()

async def main():
    """主游戏循环，适配 Pyodide 运行环境"""
    setup()
    while True:
        update_loop()
        clock.tick(FPS)  # 控制帧率
        await asyncio.sleep(1.0 / FPS)

# 适配 Pyodide 的运行方式
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())