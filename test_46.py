# -----------------------------------------------------------
# Python 创意特效：科幻传送门
#
# 教学目标：
# 1. 学习 "粒子系统" 的基本原理，用简单的对象创造复杂的效果。
# 2. 使用三角函数 (sin, cos) 来创建优雅的圆形和螺旋运动。
# 3. 学习如何管理大量对象的生命周期（创建、更新、销毁）。
# 4. 探索如何通过混合颜色和改变大小来制作动态的视觉效果。
#
# 运行方式：
# - 安装 Python 和 Pygame。
# - 将此代码保存为 a_portal_effect.py 文件。
# - 在终端或命令行中运行 `python a_portal_effect.py`。
# - 一个充满科幻感的传送门将自动出现在窗口中央！
# -----------------------------------------------------------

import pygame
import random
import math # 数学库是实现旋转效果的关键！

# --- 第一步: 初始化 Pygame 和创建窗口 ---

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800 # 使用正方形窗口，让传送门居中更好看
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("科幻传送门 - 能量漩涡")

# 定义颜色
BLACK = (0, 0, 0)
# 我们将动态生成粒子颜色，所以这里不需要预设太多

# --- 第二步: 创建一个粒子 "类" (Class) ---

# 粒子是构成传送门的基本单位。
# 每个粒子都是一个独立的小点，有自己的属性。
class Particle:
    # 构造函数：当我们创建一个新粒子时调用
    def __init__(self, x, y):
        # 粒子的初始位置 (传送门的中心)
        self.x = x
        self.y = y
        # 粒子运动的角度，随机化以从所有方向散开
        self.angle = random.uniform(0, 2 * math.pi)
        # 粒子距离中心的半径，从很小的值开始
        self.radius = random.uniform(1, 5)
        # 粒子螺旋运动的速度
        self.speed = random.uniform(0.02, 0.05)
        # 粒子的大小
        self.size = random.randint(1, 4)
        # 粒子的颜色 (这里我们用蓝紫色调，(R, G, B))
        self.color = (random.randint(100, 150), random.randint(50, 100), random.randint(200, 255))
        # 粒子的生命周期，随机化，让粒子消失的时间错开
        self.lifespan = random.uniform(80, 150)
        self.age = 0

    # 更新粒子的状态（让它运动、变老）
    def update(self):
        # 让粒子距离中心的半径慢慢变大，形成扩散效果
        self.radius += 0.5
        # 让粒子的角度不断变化，形成旋转效果
        self.angle += self.speed

        # 用三角函数计算粒子在屏幕上的新坐标
        # self.x 和 self.y 是漩涡的中心点
        # self.radius 是距离中心的距离
        # self.angle 是当前旋转到的角度
        # 这就是实现圆形/螺旋运动的数学魔法！
        self.pos_x = self.x + self.radius * math.cos(self.angle)
        self.pos_y = self.y + self.radius * math.sin(self.angle)

        # 粒子年龄增加
        self.age += 1

        # 如果粒子年龄超过其生命周期，就返回 False，表示它该被移除了
        if self.age >= self.lifespan:
            return False
        return True

    # 把粒子画在屏幕上
    def draw(self, surface):
        # 计算粒子的透明度，让它在生命尽头时逐渐消失
        # (1 - self.age / self.lifespan) 的结果是从 1 (刚出生) 慢慢变到 0 (生命尽头)
        alpha = max(0, 255 * (1 - self.age / self.lifespan))
        
        # 为了实现半透明效果，我们直接在主屏幕上画一个带 alpha 值的圆
        # 这需要屏幕支持 alpha 通道，但对于画小圆点，直接混合颜色通常也有效
        # 更准确的方法是像涟漪特效那样创建一个单独的 surface，但这里为了性能和简洁，我们简化一下
        current_color = self.color
        
        # Pygame 的 circle 不直接支持 alpha，但我们可以通过混合模式或直接画在带alpha的surface上实现
        # 这里我们用一个简单的方式，直接画实心圆
        pygame.draw.circle(surface, current_color, (int(self.pos_x), int(self.pos_y)), self.size)


# --- 第三步: 游戏主循环 ---

# 存放所有活动粒子的列表
particles = []

# 传送门的中心位置
PORTAL_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

clock = pygame.time.Clock()
running = True

while running:
    # --- 3.1: 事件处理 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- 3.2: 创建新粒子 ---
    # 为了让传送门看起来连续不断，我们每一帧都创建几个新的粒子
    # 这样即使有旧的粒子消失，也总有新的粒子补充进来
    for _ in range(5): # 每一帧创建5个粒子，可以调整这个数值来改变传送门的密度
        particles.append(Particle(PORTAL_CENTER[0], PORTAL_CENTER[1]))

    # --- 3.3: 更新和绘制 ---
    # 用纯黑色填充屏幕，但为了制造拖尾效果，我们用一个半透明的黑色
    # 创建一个和屏幕一样大的 surface
    s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    # 设置它的透明度，值越小，拖尾效果越长
    s.set_alpha(30)
    # 用纯黑色填充这个半透明的 surface
    s.fill(BLACK)
    #把它贴到主屏幕上，这样上一帧的画面就会变暗一点点，而不是完全消失
    screen.blit(s, (0, 0))

    # 更新并绘制每一个粒子
    # 我们从后往前遍历列表，这样在删除元素时不会影响后续的遍历
    for i in range(len(particles) - 1, -1, -1):
        p = particles[i]
        # 如果 update() 返回 False，说明粒子生命结束
        if not p.update():
            # 就从列表中移除它
            particles.pop(i)
        else:
            # 否则，就把它画出来
            p.draw(screen)

    # --- 3.4: 刷新显示 ---
    pygame.display.flip()

    # --- 3.5: 控制帧率 ---
    clock.tick(60)

# --- 第四步: 退出程序 ---
pygame.quit()