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
    pygame.display.set_caption("全息投影特效")
except Exception as e:
    print(f"窗口创建失败: {e}")
    import sys
    sys.exit(1)

# 定义颜色（RGB格式）
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)  # 青色，模拟全息效果
BLUE = (0, 100, 255)

# 3D点类，用于表示立方体顶点
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

# 立方体类，定义全息物体的结构
class Cube:
    def __init__(self, size):
        # 定义立方体8个顶点
        s = size / 2
        self.vertices = [
            Point3D(-s, -s, -s), Point3D(s, -s, -s), Point3D(s, s, -s), Point3D(-s, s, -s),
            Point3D(-s, -s, s), Point3D(s, -s, s), Point3D(s, s, s), Point3D(-s, s, s)
        ]
        # 定义立方体12条边（连接顶点的索引）
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # 前面
            (4, 5), (5, 6), (6, 7), (7, 4),  # 后面
            (0, 4), (1, 5), (2, 6), (3, 7)   # 连接前后
        ]
        self.color = CYAN  # 全息青色

    def update(self, time):
        # 根据时间旋转立方体
        angle_y = time * 0.5  # Y轴旋转速度
        angle_x = time * 0.3  # X轴旋转速度
        self.rotated_vertices = [v.rotate(angle_y, angle_x) for v in self.vertices]

    def draw(self, surface):
        # 绘制立方体边
        for edge in self.edges:
            point1 = self.rotated_vertices[edge[0]].project()
            point2 = self.rotated_vertices[edge[1]].project()
            # 添加动态透明度，模拟全息闪烁
            alpha = int(255 * (0.8 + 0.2 * math.sin(pygame.time.get_ticks() * 0.005)))
            color = self.color + (alpha,)
            pygame.draw.line(surface, color, point1, point2, 2)
        # 绘制顶点，增加立体感
        for point in self.rotated_vertices:
            x, y = point.project()
            pygame.draw.circle(surface, BLUE, (x, y), 4)

# 存储全息物体的列表
cubes = []

# 帧率设置
FPS = 60
clock = pygame.time.Clock()

def setup():
    # 清空立方体列表
    cubes.clear()
    # 初始化一个立方体
    cubes.append(Cube(size=1.5))
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
                # 鼠标点击添加新立方体
                cubes.append(Cube(size=random.uniform(0.5, 2.0)))

        # 清空屏幕
        screen.fill(BLACK)

        # 更新并绘制所有立方体
        for cube in cubes:
            cube.update(time)
            cube.draw(screen)

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