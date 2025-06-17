import pygame
import random
import sys
import math
import appcomm.helper.font_helper as font_helper
# 初始化pygame
pygame.init()

# 设置窗口大小和标题
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("冬日飘雪特效")

# 确保中文能正常显示
try:
    # font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 36)
    # small_font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 24)
    font = font_helper.FontHelper(None, None, 36)
    small_font = font_helper.FontHelper(None, None, 24)
except:
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)  # 天空蓝
LIGHT_BLUE = (173, 216, 230)  # 浅蓝
DARK_BLUE = (70, 130, 180)  # 深蓝
GREEN = (34, 139, 34)  # 森林绿
BROWN = (139, 69, 19)  # 棕色

# 雪花类
class Snowflake:
    def __init__(self, width, height, snow_type="normal"):
        self.x = random.randint(0, width)  # 雪花的x坐标
        self.y = random.randint(-50, 0)  # 雪花的y坐标（从屏幕上方开始）
        self.size = random.uniform(1, 5)  # 雪花大小
        self.speed = random.uniform(1, 3)  # 雪花下落速度
        self.wind = random.uniform(-0.5, 0.5)  # 风力影响（横向移动）
        self.snow_type = snow_type  # 雪花类型
        
        # 根据雪花类型设置不同的属性
        if snow_type == "big":
            self.size = random.uniform(4, 8)
            self.speed = random.uniform(2, 4)
        elif snow_type == "slow":
            self.speed = random.uniform(0.5, 1.5)
        elif snow_type == "fast":
            self.speed = random.uniform(3, 5)
        elif snow_type == "windy":
            self.wind = random.uniform(-2, 2)
            self.speed = random.uniform(1.5, 3.5)
        
        # 雪花的摆动因子
        self.swing = random.uniform(0.1, 0.5)
        self.swing_angle = random.uniform(0, 2 * math.pi)
        
        # 雪花的透明度（使大雪花更明显）
        self.alpha = int(150 + self.size * 20)
        if self.alpha > 255:
            self.alpha = 255
        
        # 创建雪花表面
        self.surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        # 绘制雪花
        if random.random() < 0.7:  # 70%的概率绘制圆形雪花
            pygame.draw.circle(
                self.surface, 
                (*WHITE[:3], self.alpha), 
                (int(self.size), int(self.size)), 
                int(self.size)
            )
        else:  # 30%的概率绘制六边形雪花
            points = []
            for i in range(6):
                angle = self.swing_angle + i * math.pi / 3
                x = self.size + self.size * 0.8 * math.cos(angle)
                y = self.size + self.size * 0.8 * math.sin(angle)
                points.append((x, y))
            pygame.draw.polygon(
                self.surface, 
                (*WHITE[:3], self.alpha), 
                points
            )

    def update(self, width, height, ground):
        # 更新雪花的摆动角度
        self.swing_angle += 0.05
        
        # 更新雪花位置（考虑风力和摆动）
        self.x += self.wind + math.sin(self.swing_angle) * self.swing
        self.y += self.speed
        
        # 检查是否触底
        if self.y >= ground:
            return False  # 雪花触底，需要移除
        
        # 检查是否超出屏幕边界
        if self.x < -20:
            self.x = width + 20
        elif self.x > width + 20:
            self.x = -20
            
        return True  # 雪花仍然在屏幕上

    def draw(self, surface):
        # 绘制雪花
        surface.blit(self.surface, (int(self.x - self.size), int(self.y - self.size)))

# 地面类（积雪效果）
class Ground:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ground_level = height * 0.8  # 地面初始高度
        self.snow_piles = [0] * width  # 记录每个x位置的积雪高度
        
        # 创建地面表面
        self.surface = pygame.Surface((width, height - int(self.ground_level)), pygame.SRCALPHA)
        self.update_surface()

    def add_snow(self, x):
        # 确保x在有效范围内
        if 0 <= x < self.width:
            # 在随机范围内增加积雪高度
            spread = random.randint(1, 3)
            for i in range(max(0, x - spread), min(self.width, x + spread + 1)):
                self.snow_piles[i] += random.uniform(0.1, 0.3)
            
            # 更新地面表面
            self.update_surface()

    def update_surface(self):
        # 清空表面
        self.surface.fill((0, 0, 0, 0))
        
        # 找到最高的积雪点
        max_snow = max(self.snow_piles)
        if max_snow > 0:
            # 绘制积雪轮廓
            points = [(0, self.height - self.ground_level)]
            for x in range(self.width):
                # 积雪高度（使用正弦函数使积雪更自然）
                snow_height = self.snow_piles[x] * (1 + 0.3 * math.sin(x * 0.05))
                points.append((x, self.height - self.ground_level - snow_height))
            points.append((self.width, self.height - self.ground_level))
            
            # 填充积雪区域
            pygame.draw.polygon(self.surface, WHITE, points)
            
            # 绘制一些阴影效果，增加立体感
            for i in range(5):
                shadow_points = [(0, self.height - self.ground_level)]
                for x in range(self.width):
                    snow_height = self.snow_piles[x] * (1 + 0.3 * math.sin(x * 0.05))
                    shadow_points.append((x, self.height - self.ground_level - snow_height + i * 0.5))
                shadow_points.append((self.width, self.height - self.ground_level))
                
                alpha = 100 - i * 20
                if alpha < 0:
                    alpha = 0
                pygame.draw.polygon(self.surface, (*WHITE[:3], alpha), shadow_points)

    def draw(self, surface):
        # 绘制地面
        surface.blit(self.surface, (0, self.ground_level))

# 树类（装饰场景）
class Tree:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.surface = pygame.Surface((size * 2, size * 3), pygame.SRCALPHA)
        self.create_tree()

    def create_tree(self):
        # 树干
        trunk_width = self.size // 4
        trunk_height = self.size
        pygame.draw.rect(
            self.surface, 
            BROWN, 
            (self.size - trunk_width // 2, self.size * 2, trunk_width, trunk_height)
        )
        
        # 树冠（多层三角形）
        for i in range(3):
            points = [
                (self.size, self.size * (2 - i)),
                (self.size - self.size * (0.8 - i * 0.2), self.size * (2.5 - i)),
                (self.size + self.size * (0.8 - i * 0.2), self.size * (2.5 - i))
            ]
            pygame.draw.polygon(self.surface, GREEN, points)
            
            # 树冠上的积雪
            snow_points = [
                (self.size, self.size * (2 - i) + self.size * 0.1),
                (self.size - self.size * (0.8 - i * 0.2), self.size * (2.2 - i)),
                (self.size + self.size * (0.8 - i * 0.2), self.size * (2.2 - i))
            ]
            pygame.draw.polygon(self.surface, WHITE, snow_points)

    def draw(self, surface):
        surface.blit(self.surface, (self.x - self.size, self.y - self.size * 3))

# 主程序
def main():
    clock = pygame.time.Clock()
    
    # 创建地面
    ground = Ground(WIDTH, HEIGHT)
    
    # 创建树木
    trees = []
    for i in range(5):
        tree_size = random.randint(40, 80)
        tree_x = random.randint(100, WIDTH - 100)
        tree_y = HEIGHT - 100
        trees.append(Tree(tree_x, tree_y, tree_size))
    
    # 雪花列表
    snowflakes = []
    snowflake_count = 200  # 初始雪花数量
    
    # 雪花类型
    snow_types = ["normal", "big", "slow", "fast", "windy"]
    current_snow_type = 0
    
    # 背景色
    bg_color = BLUE
    
    # 主循环
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:  # 增加雪花数量
                    snowflake_count = min(1000, snowflake_count + 50)
                elif event.key == pygame.K_DOWN:  # 减少雪花数量
                    snowflake_count = max(50, snowflake_count - 50)
                elif event.key == pygame.K_RIGHT:  # 切换雪花类型
                    current_snow_type = (current_snow_type + 1) % len(snow_types)
                elif event.key == pygame.K_LEFT:  # 切换雪花类型（反向）
                    current_snow_type = (current_snow_type - 1) % len(snow_types)
                elif event.key == pygame.K_c:  # 切换背景颜色
                    if bg_color == BLUE:
                        bg_color = DARK_BLUE
                    else:
                        bg_color = BLUE
        
        # 清屏
        screen.fill(bg_color)
        
        # 绘制背景（简单的渐变天空）
        for y in range(HEIGHT):
            color_value = int(235 - (y / HEIGHT) * 100)
            if color_value < 135:
                color_value = 135
            pygame.draw.line(screen, (135, color_value, 235), (0, y), (WIDTH, y), 1)
        
        # 绘制树木
        for tree in trees:
            tree.draw(screen)
        
        # 确保有足够的雪花
        while len(snowflakes) < snowflake_count:
            snowflakes.append(Snowflake(WIDTH, HEIGHT, snow_types[current_snow_type]))
        
        # 更新和绘制雪花
        new_snowflakes = []
        for snowflake in snowflakes:
            if snowflake.update(WIDTH, HEIGHT, ground.ground_level):
                snowflake.draw(screen)
                new_snowflakes.append(snowflake)
            else:
                # 雪花触底，添加到积雪中
                ground.add_snow(int(snowflake.x))
        
        snowflakes = new_snowflakes
        
        # 绘制地面（积雪）
        ground.draw(screen)
        
        # 显示信息
        small_font.render(
            f"雪花数量: {len(snowflakes)} | 雪花类型: {snow_types[current_snow_type]} | 按ESC退出",  WHITE)
        small_font.blit(screen, (20, 20))
        
        small_font.render(
            "上/下: 增加/减少雪花数量 | 左/右: 切换雪花类型 | C: 切换背景颜色", 
            WHITE
        )
        small_font.blit(screen, (20, HEIGHT - 40))
        
        # 更新屏幕
        pygame.display.flip()
        
        # 控制帧率
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
