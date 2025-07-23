# -----------------------------------------------------------
# Python 创意特效：魔法光环
#
# 教学目标：
# 1. 学习如何通过叠加半透明图形来创建 "辉光" (Glow) 效果。
# 2. 运用 sin 函数来制作平滑的、循环的 "呼吸" 动画。
# 3. 学习加载和显示外部图片 (PNG 格式)。
# 4. 理解 Surface 的使用，以及如何控制单个像素的透明度 (Alpha)。
#
# 运行方式：
# - 安装 Python 和 Pygame。
# - (可选) 准备一张名为 character.png 的图片放在同个文件夹。
# - 将此代码保存为 a_magic_aura.py 文件。
# - 在终端或命令行中运行 `python a_magic_aura.py`。
# - 一个带有魔法光环的角色将出现在窗口中央！
# -----------------------------------------------------------

import pygame
import math # sin 函数是制作呼吸效果的灵魂！

# --- 第一步: 初始化 Pygame 和创建窗口 ---

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("魔法光环 - 感受角色的力量")

# 定义颜色
BLACK = (0, 0, 0)
# 光环的颜色 (可以随意修改，比如改成火焰的橙色或自然的绿色)
AURA_COLOR = (0, 150, 255) # 一种明亮的蓝色

# --- 第二步: 加载角色图片或创建替代图形 ---

# 尝试加载外部图片
try:
    # pygame.image.load() 用来加载图片
    # .convert_alpha() 会转换图片的格式，使其在 Pygame 中绘制得更快，并且能正确处理透明部分
    character_image = pygame.image.load("character.png").convert_alpha()
    # 调整图片大小，让它适应我们的窗口
    character_image = pygame.transform.scale(character_image, (100, 100))
    print("角色图片 'character.png' 加载成功！")
except FileNotFoundError:
    # 如果找不到 "character.png" 文件，我们就自己画一个简单的图形作为替代
    print("未找到 'character.png'。正在创建一个替代图形。")
    # 创建一个和图片大小一致的 Surface (透明画布)
    character_image = pygame.Surface((100, 100), pygame.SRCALPHA)
    # 在这个画布上画一个白色的圆圈作为我们的 "角色"
    pygame.draw.circle(character_image, (255, 255, 255), (50, 50), 40, 5)

# 获取角色图片的 "矩形" 区域，这可以方便我们定位
character_rect = character_image.get_rect()
# 将角色的中心点设置在屏幕的正中央
character_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


# --- 第三步: 定义绘制光环的函数 ---

def draw_aura(surface, center, max_radius, color):
    """
    在指定的 surface 上，围绕一个中心点绘制一个辉光光环。
    - surface: 在哪个画布上绘制 (我们的主屏幕 screen)
    - center: 光环的中心点坐标 (元组)
    - max_radius: 光环的最大半径
    - color: 光环的 RGB 颜色 (元组)
    """
    # 我们从最大半径开始，向内画一系列半径递减、透明度递增的圆
    # 这样内层更亮的圆就会覆盖在外层更暗的圆之上，形成辉光效果
    num_layers = 15 # 绘制15层圆来构成光环，层数越多，光晕越柔和
    
    for i in range(num_layers, 0, -1):
        # 计算当前这一层圆的半径
        radius = max_radius * (i / num_layers)
        
        # 计算当前这一层圆的透明度 (Alpha)
        # i 越小 (越靠近中心)，alpha 越高 (越不透明)
        # 我们用一个平方根让透明度的变化更平滑
        alpha = 255 * (1 - (i / num_layers)**0.5)
        # 限制 alpha 在一个合理的范围内，避免中心完全不透明
        alpha = max(0, min(alpha, 100))

        # 创建一个临时的 Surface，它的大小刚好能容纳我们当前的圆
        # pygame.SRCALPHA 标志让这个 Surface 支持透明度
        aura_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        
        # 在这个临时 Surface 上画圆
        # 参数: (在哪里画, (R, G, B, Alpha), 中心点, 半径)
        pygame.draw.circle(
            aura_surface,
            (color[0], color[1], color[2], alpha),
            (radius, radius), # 圆心在临时 surface 的中心
            radius
        )
        
        # 最后，把这个画好了半透明圆的临时 Surface "贴" (blit) 到主屏幕上
        # 计算好粘贴的左上角位置，确保圆的中心和角色中心对齐
        surface.blit(aura_surface, (center[0] - radius, center[1] - radius))


# --- 第四步: 游戏主循环 ---

clock = pygame.time.Clock()
# time_elapsed 用于 sin 函数的计算，让动画随时间变化
time_elapsed = 0
running = True

while running:
    # --- 4.1: 事件处理 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- 4.2: 更新状态 ---
    # 增加时间计数器
    time_elapsed += clock.get_time() / 1000.0 # 转换为秒

    # 这就是 "呼吸" 效果的核心！
    # math.sin(time_elapsed) 会生成一个在 -1 和 1 之间平滑变化的数值。
    # 我们把它转换到 0 和 1 之间 ( (sin + 1) / 2 )
    # 这样我们就有了一个随时间在 0 和 1 之间平滑来回摆动的 "脉冲" 值。
    pulse = (math.sin(time_elapsed * 2) + 1) / 2 # 乘以 2 是为了让呼吸速度快一点

    # 根据脉冲值，计算光环当前帧的最大半径
    # 基础半径是40，变化幅度是20
    current_max_radius = 40 + pulse * 20

    # --- 4.3: 绘制屏幕 ---
    # 用黑色填充屏幕，清除上一帧的画面
    screen.fill(BLACK)
    
    # 绘制光环
    draw_aura(screen, character_rect.center, current_max_radius, AURA_COLOR)
    
    # 最后，在光环的上面绘制我们的角色
    # 这样角色就不会被光环覆盖了
    screen.blit(character_image, character_rect)

    # --- 4.4: 刷新显示 ---
    pygame.display.flip()

    # --- 4.5: 控制帧率 ---
    clock.tick(60)

# --- 第五步: 退出程序 ---
pygame.quit()