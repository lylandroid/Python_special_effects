import pygame
import platform
import asyncio
import colorsys
import math
import appcomm
import appcomm.helper
import appcomm.helper.font_helper

# 初始化Pygame
pygame.init()

# 设置屏幕尺寸
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("曼德布罗特分形幻想")

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 分形参数
max_iterations = 100  # 最大迭代次数，控制分形细节
zoom = 1.0  # 缩放比例
x_offset, y_offset = -0.5, 0.0  # 平移偏移量
zoom_speed = 0.1  # 缩放速度
move_speed = 0.1  # 平移速度

# 帧率控制
FPS = 30
clock = pygame.time.Clock()

def setup():
    # 设置背景颜色
    screen.fill(BLACK)

def mandelbrot(c, max_iter):
    # 计算曼德布罗特分形点是否在集合内
    z = 0
    for i in range(max_iter):
        z = z * z + c  # 曼德布罗特迭代公式：z = z^2 + c
        if abs(z) > 2:  # 如果|z|>2，点不在集合内
            # 使用颜色平滑算法，生成更平滑的颜色过渡
            smooth = i + 1 - math.log(math.log2(abs(z))) if abs(z) > 0 else i
            hue = smooth / max_iter  # 色调基于迭代次数
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0 if i < max_iter else 0.0)
            return [int(c * 255) for c in rgb]  # 转换为RGB颜色
    return BLACK  # 在集合内的点为黑色

def draw_mandelbrot(zoom, x_offset, y_offset):
    # 绘制曼德布罗特分形
    for x in range(WIDTH):
        for y in range(HEIGHT):
            # 将屏幕坐标映射到复平面
            real = (x - WIDTH / 2) / (0.5 * zoom * WIDTH) + x_offset
            imag = (y - HEIGHT / 2) / (0.5 * zoom * HEIGHT) + y_offset
            c = complex(real, imag)  # 复数c
            color = mandelbrot(c, max_iterations)  # 计算颜色
            screen.set_at((x, y), color)  # 设置像素颜色

def update_loop():
    global zoom, x_offset, y_offset, max_iterations

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                zoom *= (1 + zoom_speed)  # 放大
            if event.key == pygame.K_MINUS:
                zoom /= (1 + zoom_speed)  # 缩小
            if event.key == pygame.K_UP:
                y_offset -= move_speed / zoom  # 向上平移
            if event.key == pygame.K_DOWN:
                y_offset += move_speed / zoom  # 向下平移
            if event.key == pygame.K_LEFT:
                x_offset -= move_speed / zoom  # 向左平移
            if event.key == pygame.K_RIGHT:
                x_offset += move_speed / zoom  # 向右平移
            if event.key == pygame.K_i:
                max_iterations += 10  # 增加迭代次数，增强细节
            if event.key == pygame.K_o and max_iterations > 10:
                max_iterations -= 10  # 减少迭代次数

    # 清屏
    screen.fill(BLACK)

    # 绘制分形
    draw_mandelbrot(zoom, x_offset, y_offset)

    # 添加操作提示文本
    # font = pygame.font.Font(None, 36)
    font = appcomm.helper.font_helper.FontHelper(None,None,36)
    # text = font.render("+/-: 缩放  上下左右: 移动  i/o: 调整细节", True, WHITE)
    # screen.blit(text, (10, 10))
    font.render("+/-: 缩放  上下左右: 移动  i/o: 调整细节", WHITE)
    font.blit(screen, (10, 10))

    # 更新屏幕
    pygame.display.flip()

async def main():
    setup()  # 初始化游戏
    while True:
        update_loop()  # 更新分形
        await asyncio.sleep(1.0 / FPS)  # 控制帧率

# 检查是否在Pyodide环境中运行
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())