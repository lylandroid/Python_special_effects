# 导入 pygame 库，它是我们制作游戏和动画的魔法工具箱
import pygame
# 导入 random 库，用来添加一些随机性，让烟雾看起来更自然
import random
# 导入 math 库，用来做一些数学计算，比如旋转
import math

# --- 1. 初始化设置：搭建我们的魔法舞台 ---

# 初始化 pygame 的所有模块，这是每次使用前必须做的准备工作
pygame.init()

# 设置我们魔法舞台（屏幕）的宽度和高度
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 创建一个指定大小的屏幕对象
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# 设置窗口的标题，告诉世界我们正在施展什么魔法
pygame.display.set_caption("Python 创意特效 - 旋转的神秘烟雾")

# 定义颜色 (使用RGB颜色模式)
# 我们用纯黑色作为背景，这样白色的烟雾会非常显眼
BLACK = (0, 0, 0)
# 我们会用不同深浅的灰色来组成烟雾
GRAY_SHADES = [(220, 220, 220), (200, 200, 200), (180, 180, 180)]

# 创建一个时钟对象，它可以帮助我们控制动画的刷新速度（帧率）
clock = pygame.time.Clock()


# --- 2. 定义“烟雾颗粒”：创造烟雾的基本元素 ---

# 我们用一个“类(Class)”来定义每一个烟雾颗粒的行为和外观
# 可以把它想象成是创造“烟雾小精灵”的蓝图
class SmokeParticle:
    def __init__(self, x, y):
        # 每个小精灵一出生就在屏幕中心 (x, y)
        self.x = x
        self.y = y
        # 初始半径，随机大小让烟雾更有层次感
        self.radius = random.randint(5, 15)
        # 初始颜色，从我们预设的灰色中随机选一种
        self.color = random.choice(GRAY_SHADES)
        # 核心！alpha值代表透明度，255是完全不透明，0是完全透明
        # 初始透明度也是随机的，让烟雾有浓有淡
        self.alpha = random.randint(100, 200)

        # --- 决定小精灵的运动轨迹 ---
        # 初始的旋转角度
        self.angle = random.uniform(0, 2 * math.pi)
        # 飞行的速度
        self.speed = random.uniform(1, 3)

    # 这个函数负责更新每个小精灵的状态（位置、大小、透明度）
    def update(self):
        # 使用三角函数（sin和cos）根据角度和速度计算出新的位置，实现旋转扩散
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # 让角度也随机变化一点，轨迹就不会是完美的圆形，更像真实的烟雾
        self.angle += random.uniform(-0.1, 0.1)

        # 随着时间流逝，小精灵会慢慢变淡（透明度降低）
        self.alpha -= 2 # 这个值越小，烟雾消失得越慢
        # 同时，小精灵的身体会慢慢变大，模拟烟雾扩散的效果
        self.radius += 0.5

    # 这个函数负责把小精灵画在我们的魔法舞台上
    def draw(self, surface):
        # 我们不能直接画带透明度的圆，需要一个小技巧
        # 1. 创建一个和颗粒一样大的、完全透明的临时小画布 (SRCALPHA)
        temp_surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        # 2. 在这个小画布的中心，画上我们的烟雾颗粒
        #    颜色是 (R, G, B, Alpha)，这里的 alpha 就是我们的透明度
        pygame.draw.circle(temp_surf, (*self.color, self.alpha), (self.radius, self.radius), self.radius)
        # 3. 把这个画好了的小画布，贴到我们的大舞台上
        surface.blit(temp_surf, (self.x - self.radius, self.y - self.radius))


# --- 3. 主循环：让魔法持续上演 ---

# 创建一个列表，用来存放所有活着的“烟雾小精灵”
particles = []

# running 是一个标记，只要它为 True，我们的魔法就会一直进行
running = True
while running:
    # --- 事件处理：与外界互动 ---
    # 检查所有用户事件（比如点击鼠标、关闭窗口）
    for event in pygame.event.get():
        # 如果用户点击了窗口的关闭按钮
        if event.type == pygame.QUIT:
            running = False # 将标记设为 False，结束循环

    # --- 生成新的烟雾 ---
    # 每一帧都在屏幕中心生成3个新的烟雾颗粒，让烟雾源源不断
    for _ in range(3):
        p = SmokeParticle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        particles.append(p)

    # --- 更新和绘制 ---
    # 用纯黑色填充整个屏幕，盖住上一帧的画面
    screen.fill(BLACK)

    # 遍历列表里每一个“烟雾小精灵”
    # 注意：我们遍历列表的副本(particles[:])，因为我们可能会在循环中删除元素
    for p in particles[:]:
        # 更新它的状态
        p.update()
        # 如果小精灵已经完全透明（消失了）
        if p.alpha <= 0:
            # 就把它从列表中移除，减轻程序负担
            particles.remove(p)
        else:
            # 否则，就把它画出来
            p.draw(screen)

    # --- 刷新屏幕 ---
    # 将我们这一帧画的所有东西，一次性更新到屏幕上
    pygame.display.flip()

    # 控制动画的帧率，让它在不同性能的电脑上速度都差不多
    # 60 代表每秒刷新60次
    clock.tick(60)

# --- 魔法结束 ---
# 退出 pygame，释放所有资源
pygame.quit()