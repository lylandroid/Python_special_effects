import pygame
import math
import random
import asyncio
import platform
import sys

# 初始化Pygame，准备绘图环境
try:
    pygame.init()
except Exception as e:
    print(f"Pygame初始化失败: {e}")
    sys.exit(1)

# 设置窗口大小和渲染分辨率（降低分辨率以提高性能）
WIDTH, HEIGHT = 800, 600
RENDER_WIDTH, RENDER_HEIGHT = 200, 150  # 降低渲染分辨率
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    render_surface = pygame.Surface((RENDER_WIDTH, RENDER_HEIGHT))  # 创建渲染表面
    pygame.display.set_caption("简易光线追踪特效（优化版）")
except Exception as e:
    print(f"窗口创建失败: {e}")
    sys.exit(1)

# 定义颜色（RGB格式）
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 向量类，用于处理3D向量运算
class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def normalize(self):
        mag = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        return Vector3(self.x / mag, self.y / mag, self.z / mag) if mag != 0 else Vector3(0, 0, 0)

# 球体类，用于定义场景中的物体
class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

    def intersect(self, ray_origin, ray_dir):
        oc = ray_origin - self.center
        a = ray_dir.dot(ray_dir)
        b = 2.0 * oc.dot(ray_dir)
        c = oc.dot(oc) - self.radius**2
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            return None
        t = (-b - math.sqrt(discriminant)) / (2.0 * a)
        return t if t > 0 else None

# 光源类
class Light:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

# 场景设置
camera = Vector3(0, 0, -5)
sphere = Sphere(Vector3(0, 0, 0), 1, RED)
light = Light(Vector3(2, 2, -5), 1.0)

# 帧率设置
FPS = 30
clock = pygame.time.Clock()

def setup():
    # 清空渲染表面
    render_surface.fill(BLACK)
    screen.fill(BLACK)

def trace_ray(x, y, time):
    # 将渲染表面坐标转换为3D光线方向
    aspect_ratio = RENDER_WIDTH / RENDER_HEIGHT
    px = (2 * (x + 0.5) / RENDER_WIDTH - 1) * aspect_ratio
    py = 1 - 2 * (y + 0.5) / RENDER_HEIGHT
    ray_dir = Vector3(px, py, 1).normalize()

    # 检查光线与球体交点
    t = sphere.intersect(camera, ray_dir)
    if t is None:
        return BLACK

    # 计算交点、光照
    hit_point = Vector3(
        camera.x + t * ray_dir.x,
        camera.y + t * ray_dir.y,
        camera.z + t * ray_dir.z
    )
    normal = (hit_point - sphere.center).normalize()
    light.position = Vector3(
        2 * math.cos(time),
        2 * math.sin(time),
        -5
    )
    light_dir = (light.position - hit_point).normalize()
    diffuse = max(0, normal.dot(light_dir)) * light.intensity
    color = (
        int(sphere.color[0] * diffuse),
        int(sphere.color[1] * diffuse),
        int(sphere.color[2] * diffuse)
    )
    return color

def update_loop(time):
    try:
        # 清空渲染表面
        render_surface.fill(BLACK)

        # 逐像素光线追踪（低分辨率）
        for y in range(RENDER_HEIGHT):
            for x in range(RENDER_WIDTH):
                color = trace_ray(x, y, time)
                render_surface.set_at((x, y), color)

        # 放大渲染表面到全屏
        screen.blit(pygame.transform.scale(render_surface, (WIDTH, HEIGHT)), (0, 0))

        # 更新屏幕
        pygame.display.flip()
    except Exception as e:
        print(f"渲染失败: {e}")

async def main():
    setup()
    time = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

        update_loop(time)
        time += 0.1
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

# 适配Pyodide环境
if platform.system() == "Emscripten":
    try:
        asyncio.ensure_future(main())
    except Exception as e:
        print(f"异步循环启动失败: {e}")
else:
    if __name__ == "__main__":
        asyncio.run(main())