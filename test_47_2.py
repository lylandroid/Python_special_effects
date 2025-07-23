import pygame
import math
import asyncio
import platform

# 初始化 Pygame
pygame.init()

# 设置窗口大小
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("魔法光环 - 角色发光特效")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GLOW_PURPLE = (200, 100, 255)  # 光环的主色调（紫色）
GLOW_BLUE = (100, 150, 255)    # 光环的辅助色（蓝色）

# 帧率控制
FPS = 60
clock = pygame.time.Clock()

# 角色位置和光环参数
player_pos = [WIDTH // 2, HEIGHT // 2]  # 角色初始位置（屏幕中心）
aura_radius = 50  # 光环半径
pulse_speed = 0.05  # 光环脉动速度
pulse_amplitude = 10  # 光环脉动幅度

def draw_player(surface, pos):
    """绘制角色（简单圆形）"""
    pygame.draw.circle(surface, WHITE, pos, 20)  # 绘制白色圆形作为角色

def draw_aura(surface, pos, time):
    """绘制动态魔法光环"""
    # 计算脉动效果，改变光环半径
    pulse = math.sin(time * pulse_speed) * pulse_amplitude
    current_radius = aura_radius + pulse
    
    # 绘制多层光环，创建渐变效果
    for i in range(5, 0, -1):
        # 每层光环半径逐渐减小，透明度递增
        radius = current_radius + i * 5
        alpha = 100 // i  # 透明度递减
        # 创建临时表面以支持透明度
        temp_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        # 混合紫色和蓝色光环颜色
        color = (
            int(GLOW_PURPLE[0] * (i / 5) + GLOW_BLUE[0] * (1 - i / 5)),
            int(GLOW_PURPLE[1] * (i / 5) + GLOW_BLUE[1] * (1 - i / 5)),
            int(GLOW_PURPLE[2] * (i / 5) + GLOW_BLUE[2] * (1 - i / 5))
        )
        pygame.draw.circle(temp_surface, color + (alpha,), (radius, radius), radius)
        # 将光环绘制到屏幕上
        surface.blit(temp_surface, (pos[0] - radius, pos[1] - radius))

def setup():
    """初始化游戏设置"""
    screen.fill(BLACK)  # 清空屏幕为黑色背景

def update_loop():
    """更新游戏状态"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
    # 获取鼠标位置，让角色跟随鼠标
    player_pos[0], player_pos[1] = pygame.mouse.get_pos()
    
    # 清空屏幕
    screen.fill(BLACK)
    # 获取当前时间用于光环动画
    time = pygame.time.get_ticks() / 1000.0
    # 绘制光环和角色
    draw_aura(screen, player_pos, time)
    draw_player(screen, player_pos)
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