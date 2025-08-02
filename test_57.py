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
    pygame.display.set_caption("AR叠加 - 虚拟物体特效")
except Exception as e:
    print(f"窗口创建失败: {e}")
    import sys
    sys.exit(1)

# 定义颜色（RGB格式）
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)

# 创建模拟的“现实世界”背景
def create_background():
    # 创建一个表面模拟现实世界的背景
    background = pygame.Surface((WIDTH, HEIGHT))
    # 用渐变色填充，模拟自然场景
    for y in range(HEIGHT):
        # 从蓝色（天空）渐变到绿色（地面）
        color = (
            int(50 + 100 * (1 - y / HEIGHT)),  # R
            int(100 + 100 * (y / HEIGHT)),     # G
            int(150 - 50 * (y / HEIGHT))       # B
        )
        pygame.draw.line(background, color, (0, y), (WIDTH, y))
    # 添加随机“物体”模拟现实场景
    for _ in range(50):
        x = random.randint(0, WIDTH)
        y = random.randint(HEIGHT // 2, HEIGHT)
        radius = random.randint(5, 20)
        pygame.draw.circle(background, WHITE, (x, y), radius)
    return background

# 3D点类，用于表示虚拟物体的顶点
class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # 旋转点（绕Y轴和X轴）
    def rotate(self, angle_y, angle_x):
        # 绕Y轴旋转
        cos_y = math.cos(angle_y)
        sin_y = math.sin(angle_y)
        x = self.x * cos_y + self.z * sin_y
        z = -self.x * sin_y + self.z * cos_y
        # 绕X轴旋转
        cos_x = math.cos(angle_x)
        sin_x = math.sin(angle_x)
        y = self.y * cos_x - z * sin_x
        z = self.y * sin_x + z * cos_x
        return Point3D(x, y, z)

    # 透视投影到2D
    def project(self, fov=500, viewer_distance=4):
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + WIDTH / 2
        y = -self.y * factor + HEIGHT / 2
        return (int(x), int(y))

# 虚拟立方体类，模拟AR中的虚拟物体
class Cube:
    def __init__(self, x, y, z, size):
        self.center = Point3D(x, y, z)
        s = size / 2
        # 定义立方体8个顶点（相对于中心）
        self.vertices = [
            Point3D(x + dx, y + dy, z + dz)
            for dx in [-s, s] for dy in [-s, s] for dz in [-s, s]
        ]
        # 定义立方体12条边
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # 前面
            (4, 5), (5, 6), (6, 7), (7, 4),  # 后面
            (0, 4), (1, 5), (2, 6), (3, 7)   # 连接前后
        ]
        self.color = CYAN  # AR虚拟物体颜色

    def update(self, time):
        # 旋转立方体
        angle_y = time * 0.5
        angle_x = time * 0.3
        self.rotated_vertices = [v.rotate(angle_y, angle_x) for v in self.vertices]

    def draw(self, surface):
        # 创建临时表面支持透明度
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # 绘制立方体边
        for edge in self.edges:
            point1 = self.rotated_vertices[edge[0]].project()
            point2 = self.rotated_vertices[edge[1]].project()
            # 动态透明度，模拟AR光晕
            alpha = int(255 * (0.7 + 0.3 * math.sin(pygame.time.get_ticks() * 0.005)))
            color = self.color + (alpha,)
            pygame.draw.line(temp_surface, color, point1, point2, 2)
        # 绘制顶点
        for vertex in self.rotated_vertices:
            x, y = vertex.project()
            pygame.draw.circle(temp_surface, YELLOW, (x, y), 4)
        # 将临时表面叠加到主屏幕
        surface.blit(temp_surface, (0, 0))

# 存储虚拟物体
cubes = []

# 帧率设置
FPS = 60
clock = pygame.time.Clock()

def setup():
    # 清空立方体列表
    cubes.clear()
    # 初始化一个虚拟立方体
    cubes.append(Cube(x=0, y=0, z=0, size=1.0))
    # 创建背景
    global background
    background = create_background()

def update_loop(time):
    try:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标点击添加新立方体
                x, y = pygame.mouse.get_pos()
                # 将2D鼠标坐标映射到3D空间
                z = random.uniform(-1, 1)
                cubes.append(Cube(x=0, y=0, z=z, size=random.uniform(0.5, 1.5)))

        # 绘制背景
        screen.blit(background, (0, 0))

        # 更新并绘制虚拟立方体
        for cube in cubes:
            cube.update(time)
            cube.draw(screen)

        # 更新屏幕
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
        time += 0.1  # 控制旋转速度
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