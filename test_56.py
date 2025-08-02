import pygame
import math
import random
import asyncio
import platform

WHITE = (255, 255, 255)

# 初始化Pygame，准备绘图环境
try:
    pygame.init()
except Exception as e:
    print(f"Pygame初始化失败: {e}")
    import sys
    sys.exit(1)

# 设置窗口大小（模拟VR双目显示，左右各半屏）
WIDTH, HEIGHT = 800, 600
HALF_WIDTH = WIDTH // 2
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("VR一瞥 - 简单虚拟现实场景")
except Exception as e:
    print(f"窗口创建失败: {e}")
    import sys
    sys.exit(1)

# 定义颜色（RGB格式）
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)

# 3D点类，用于表示球体顶点
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

    # 透视投影到2D（模拟VR视角）
    def project(self, fov=500, viewer_distance=4, eye_offset=0):
        factor = fov / (viewer_distance + self.z)
        x = (self.x + eye_offset) * factor + HALF_WIDTH / 2
        y = -self.y * factor + HEIGHT / 2
        return (int(x), int(y))

# 球体类，模拟VR场景中的3D物体
class Sphere:
    def __init__(self, radius, segments):
        self.radius = radius
        self.segments = segments
        self.vertices = []
        self.color = CYAN
        # 生成球体顶点（使用参数化方程）
        for i in range(segments + 1):
            phi = i * math.pi / segments
            for j in range(segments * 2 + 1):
                theta = j * 2 * math.pi / (segments * 2)
                x = radius * math.sin(phi) * math.cos(theta)
                y = radius * math.sin(phi) * math.sin(theta)
                z = radius * math.cos(phi)
                self.vertices.append(Point3D(x, y, z))
        # 定义连接线（简化，仅绘制经纬线）
        self.edges = []
        for i in range(segments):
            for j in range(segments * 2):
                v0 = i * (segments * 2 + 1) + j
                v1 = v0 + 1
                v2 = (i + 1) * (segments * 2 + 1) + j
                self.edges.append((v0, v1))
                self.edges.append((v0, v2))

    def update(self, time):
        # 旋转球体
        angle_y = time * 0.4  # Y轴旋转速度
        angle_x = time * 0.3  # X轴旋转速度
        self.rotated_vertices = [v.rotate(angle_y, angle_x) for v in self.vertices]

    def draw(self, surface, eye_offset, x_offset):
        # 绘制球体（针对左眼或右眼）
        for edge in self.edges:
            point1 = self.rotated_vertices[edge[0]].project(eye_offset=eye_offset)
            point2 = self.rotated_vertices[edge[1]].project(eye_offset=eye_offset)
            # 动态透明度，模拟VR光晕
            alpha = int(255 * (0.7 + 0.3 * math.sin(pygame.time.get_ticks() * 0.005)))
            color = self.color + (alpha,)
            pygame.draw.line(surface, color, 
                            (point1[0] + x_offset, point1[1]), 
                            (point2[0] + x_offset, point2[1]), 1)

# 存储场景物体
spheres = []

# 帧率设置
FPS = 60
clock = pygame.time.Clock()

def setup():
    # 清空球体列表
    spheres.clear()
    # 初始化一个球体
    spheres.append(Sphere(radius=1.0, segments=10))
    # 设置背景颜色
    screen.fill(BLACK)

def update_loop(time):
    try:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标点击添加新球体
                spheres.append(Sphere(
                    radius=random.uniform(0.5, 1.5),
                    segments=10
                ))

        # 清空屏幕
        screen.fill(BLACK)

        # 创建左右眼表面
        left_eye_surface = pygame.Surface((HALF_WIDTH, HEIGHT), pygame.SRCALPHA)
        right_eye_surface = pygame.Surface((HALF_WIDTH, HEIGHT), pygame.SRCALPHA)

        # 更新并绘制球体（左右眼偏移）
        for sphere in spheres:
            sphere.update(time)
            sphere.draw(left_eye_surface, eye_offset=-0.1, x_offset=0)  # 左眼
            sphere.draw(right_eye_surface, eye_offset=0.1, x_offset=0)  # 右眼

        # 将左右眼画面合并到主屏幕
        screen.blit(left_eye_surface, (0, 0))
        screen.blit(right_eye_surface, (HALF_WIDTH, 0))
        # 绘制分隔线
        pygame.draw.line(screen, WHITE, (HALF_WIDTH, 0), (HALF_WIDTH, HEIGHT), 2)

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