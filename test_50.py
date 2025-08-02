import pygame
import platform
import asyncio
import random
import math
import appcomm
import appcomm.app
import appcomm.app.app_pygame_class
import appcomm.helper
import appcomm.helper.font_helper

# 初始化Pygame
pygame.init()

# 设置屏幕尺寸
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("时间静止特效")

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# 球的初始参数
ball_x = WIDTH // 2  # 球的初始x坐标
ball_y = HEIGHT // 2  # 球的初始y坐标
ball_radius = 20  # 球的半径
ball_speed_x = 5  # 球的x方向速度
ball_speed_y = 3  # 球的y方向速度

# 时间静止效果参数
is_time_stopped = False  # 是否处于时间静止状态
stop_duration = 120  # 时间静止持续帧数
stop_timer = 0  # 时间静止计时器
shake_amplitude = 5  # 震动幅度
fade_alpha = 100  # 渐变透明度

# 帧率控制
FPS = 60
clock = pygame.time.Clock()

def setup():
    # 设置背景颜色
    screen.fill(BLACK)

def update_loop():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    global is_time_stopped, stop_timer, fade_alpha

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # 按空格键触发时间静止
                is_time_stopped = True
                stop_timer = stop_duration

    # 清屏
    screen.fill(BLACK)

    if is_time_stopped:
        # 时间静止状态
        stop_timer -= 1
        if stop_timer <= 0:
            is_time_stopped = False  # 结束时间静止
            fade_alpha = 100  # 重置透明度

        # 添加震动效果
        shake_x = random.uniform(-shake_amplitude, shake_amplitude)
        shake_y = random.uniform(-shake_amplitude, shake_amplitude)
        # 绘制半透明背景，模拟渐变效果
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(fade_alpha)
        overlay.fill(BLUE)
        screen.blit(overlay, (0, 0))
        fade_alpha = max(50, fade_alpha - 2)  # 逐渐减小透明度
        # 绘制震动的球
        pygame.draw.circle(screen, RED, (int(ball_x + shake_x), int(ball_y + shake_y)), ball_radius)
    else:
        # 正常移动状态
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # 边界碰撞检测
        if ball_x - ball_radius < 0 or ball_x + ball_radius > WIDTH:
            ball_speed_x = -ball_speed_x
        if ball_y - ball_radius < 0 or ball_y + ball_radius > HEIGHT:
            ball_speed_y = -ball_speed_y

        # 绘制移动的球
        pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)

    # 添加时间静止提示文本
    # font = pygame.font.Font(None, 36)
    font = appcomm.helper.font_helper.FontHelper(None,None,24)
    font.render("按空格键触发时间静止！", WHITE)
    # text = font.render("按空格键触发时间静止！", True, WHITE)
    # screen.blit(text, (10, 10))
    font.blit(screen,(10, 10))

    # 更新屏幕
    pygame.display.flip()

async def main():
    setup()  # 初始化游戏
    while True:
        update_loop()  # 更新游戏状态
        await asyncio.sleep(1.0 / FPS)  # 控制帧率

# 检查是否在Pyodide环境中运行
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())