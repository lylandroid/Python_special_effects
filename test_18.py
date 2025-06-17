# ----------------------------------------------------
# Python 少儿编程 - 创意特效：闪烁的火焰
#
# 这个项目会教我们：
# 1. 如何用“粒子系统”来模拟复杂的动态效果，比如火焰。
# 2. 如何通过一个预设的颜色列表，让粒子在生命周期中平滑地改变颜色。
# 3. 如何让粒子在消失时逐渐变小，创造更自然的效果。
# 4. 这是一个综合性的小项目，能很好地锻炼我们的编程思维。
# ----------------------------------------------------

# 导入我们需要的库
import pygame
import random

# --- 1. 初始化 Pygame 和设置 ---
pygame.init()

# 设置窗口的宽度和高度
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800 # 高一点的窗口更适合火焰
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("闪烁的火焰特效 by Gemini")

# 定义颜色
# 我们用一个非常深的红色作为背景，来突出火焰的光辉
BACKGROUND_COLOR = (20, 0, 0)
# 这就是我们火焰的“调色盘”，从最亮到最暗
FIRE_COLORS = [
    (255, 255, 200),  # 亮黄色 (火焰核心)
    (255, 180, 0),    # 橙黄色
    (255, 100, 0),    # 橙色
    (200, 50, 0),     # 深橙色
    (100, 0, 0)       # 暗红色 (火焰边缘)
]

# 创建时钟对象
clock = pygame.time.Clock()

# --- 2. 创建火焰粒子类 (FlameParticle Class) ---
class FlameParticle:
    # 构造函数：当一个新火星被创建时调用
    def __init__(self, x, y):
        # 初始位置在火焰底部
        self.x = x
        self.y = y
        
        # 水平速度，用来模拟火焰的左右摇曳
        self.vx = random.uniform(-0.8, 0.8)
        # 垂直速度，负数代表向上移动
        self.vy = random.uniform(-4, -2)
        
        # 初始大小
        self.size = random.randint(15, 25)
        
        # 生命值：一个粒子能存在多久
        # 我们让它和大小相关，大粒子活得久一点，飘得高一点
        self.lifespan = self.size * 4
        # 保存初始生命值，后面计算颜色时会用到
        self.initial_lifespan = self.lifespan

    # 更新粒子的状态
    def update(self):
        # 根据速度更新位置
        self.x += self.vx
        self.y += self.vy
        
        # 生命值不断减少
        self.lifespan -= 1
        
        # 粒子随着上升，不断变小
        if self.size > 0:
            self.size -= 0.2

    # 在屏幕上绘制粒子
    def draw(self, surface):
        # 只有当粒子还“活着”并且还看得见时才绘制
        if self.lifespan > 0 and self.size > 0:
            # --- 颜色变化的核心魔法 ---
            # 1. 计算粒子生命还剩下百分之多少 (范围从 1.0 到 0.0)
            life_percent = self.lifespan / self.initial_lifespan
            
            # 2. 根据生命百分比，我们想从 FIRE_COLORS 列表中选择一个颜色
            # life_percent 从 1.0 降到 0.0，所以我们用 (1 - life_percent) 把它反过来
            # (1 - life_percent) 会从 0.0 增长到 1.0
            color_index = (1 - life_percent) * (len(FIRE_COLORS) - 1)
            
            # 3. 把它变成整数，作为列表的索引
            color_index = min(int(color_index), len(FIRE_COLORS) - 1)
            
            # 4. 从我们的调色盘中获取最终颜色
            final_color = FIRE_COLORS[color_index]

            # 绘制一个圆形来代表火星粒子
            pygame.draw.circle(surface, final_color, (int(self.x), int(self.y)), int(self.size))


# --- 3. 主循环 ---
# 创建一个列表来存放所有的火焰粒子
particles = []

# 火焰的根部在屏幕底部中央
fire_base_x = SCREEN_WIDTH // 2
fire_base_y = SCREEN_HEIGHT - 50

running = True
while running:
    # --- a. 事件处理 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- b. 创建新的粒子 ---
    # 每一帧都创建一些新的粒子，来维持火焰的燃烧
    # 调整 range() 里的数字可以控制火焰的大小
    for _ in range(8):
        # 让新粒子在火焰根部的一个小范围内随机出现
        px = fire_base_x + random.randint(-20, 20)
        py = fire_base_y + random.randint(-10, 10)
        particles.append(FlameParticle(px, py))

    # --- c. 更新和绘制 ---
    # 用背景色填充屏幕
    screen.fill(BACKGROUND_COLOR)

    # 遍历列表的一个副本 (particles[:])，因为我们可能会在循环中删除元素
    for p in particles[:]:
        p.update() # 更新粒子的状态
        p.draw(screen) # 绘制粒子
        
        # 如果粒子的生命结束了，就从列表中移除它
        if p.lifespan <= 0:
            particles.remove(p)

    # --- d. 刷新屏幕 ---
    pygame.display.flip()

    # --- e. 控制帧率 ---
    clock.tick(60)

# --- 5. 退出程序 ---
pygame.quit()