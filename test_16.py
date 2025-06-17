import pygame
import math
import time
import random
import sys

# 初始化pygame
pygame.init()

# 设置窗口大小和标题
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("活灵活现的模拟时钟")

# 确保中文能正常显示
try:
    font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 36)
    small_font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 24)
except:
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# 时钟样式列表
CLOCK_STYLES = [
    {"name": "经典黑", "bg_color": (240, 240, 240), "clock_color": BLACK, "hour_color": BLACK, 
     "minute_color": (50, 50, 50), "second_color": RED, "tick_color": (100, 100, 100)},
    
    {"name": "彩虹炫彩", "bg_color": (240, 240, 240), "clock_color": (0, 0, 0), 
     "hour_color": RED, "minute_color": BLUE, "second_color": GREEN, "tick_color": (100, 100, 100)},
    
    {"name": "星空", "bg_color": (10, 10, 30), "clock_color": WHITE, "hour_color": YELLOW, 
     "minute_color": CYAN, "second_color": PURPLE, "tick_color": WHITE},
    
    {"name": "海洋", "bg_color": (10, 30, 60), "clock_color": CYAN, "hour_color": BLUE, 
     "minute_color": (0, 100, 200), "second_color": WHITE, "tick_color": (100, 200, 255)},
    
    {"name": "森林", "bg_color": (20, 50, 20), "clock_color": GREEN, "hour_color": (0, 100, 0), 
     "minute_color": (50, 150, 50), "second_color": YELLOW, "tick_color": (100, 200, 100)}
]

# 粒子类 - 用于时钟周围的装饰效果
class Particle:
    def __init__(self, x, y, color, clock_radius):
        self.x = x
        self.y = y
        self.color = color
        self.radius = random.randint(1, 3)
        self.speed = random.uniform(0.5, 2)
        self.angle = random.uniform(0, 2 * math.pi)
        self.clock_radius = clock_radius
        self.life = random.randint(30, 120)  # 粒子生命周期

    def update(self):
        # 粒子向外扩散
        self.clock_radius += self.speed
        self.x = WIDTH // 2 + self.clock_radius * math.cos(self.angle)
        self.y = HEIGHT // 2 + self.clock_radius * math.sin(self.angle)
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        # 绘制粒子
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

# 主程序
def main():
    clock = pygame.time.Clock()
    particles = []  # 存储所有粒子
    current_style = 0  # 当前时钟样式索引
    show_seconds = True  # 是否显示秒针
    show_date = True  # 是否显示日期
    show_info = True  # 是否显示信息面板
    particle_enabled = True  # 是否启用粒子效果
    
    # 主循环
    running = True
    while running:
        # 获取当前时间
        current_time = time.localtime()
        hour = current_time.tm_hour % 12
        minute = current_time.tm_min
        second = current_time.tm_sec
        day = current_time.tm_mday
        month = current_time.tm_mon
        year = current_time.tm_year
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:  # 空格键切换时钟样式
                    current_style = (current_style + 1) % len(CLOCK_STYLES)
                elif event.key == pygame.K_s:  # S键切换秒针显示
                    show_seconds = not show_seconds
                elif event.key == pygame.K_d:  # D键切换日期显示
                    show_date = not show_date
                elif event.key == pygame.K_i:  # I键切换信息显示
                    show_info = not show_info
                elif event.key == pygame.K_p:  # P键切换粒子效果
                    particle_enabled = not particle_enabled
        
        # 清屏
        screen.fill(CLOCK_STYLES[current_style]["bg_color"])
        
        # 时钟中心位置
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        clock_radius = min(WIDTH, HEIGHT) // 3
        
        # 绘制时钟外圈
        pygame.draw.circle(screen, CLOCK_STYLES[current_style]["clock_color"], 
                          (center_x, center_y), clock_radius, 3)
        
        # 绘制时钟刻度
        for i in range(60):
            angle = i * math.pi / 30
            if i % 5 == 0:  # 小时刻度
                length = clock_radius * 0.15
                width = 5
            else:  # 分钟刻度
                length = clock_radius * 0.1
                width = 2
                
            start_x = center_x + (clock_radius - length) * math.sin(angle)
            start_y = center_y - (clock_radius - length) * math.cos(angle)
            end_x = center_x + clock_radius * math.sin(angle)
            end_y = center_y - clock_radius * math.cos(angle)
            
            pygame.draw.line(screen, CLOCK_STYLES[current_style]["tick_color"],
                            (start_x, start_y), (end_x, end_y), width)
        
        # 绘制时钟数字
        for i in range(12):
            angle = i * math.pi / 6
            number_x = center_x + (clock_radius * 0.8) * math.sin(angle)
            number_y = center_y - (clock_radius * 0.8) * math.cos(angle)
            
            number_text = str(i + 1 if i != 0 else 12)
            text_surface = font.render(number_text, True, CLOCK_STYLES[current_style]["clock_color"])
            text_rect = text_surface.get_rect(center=(number_x, number_y))
            screen.blit(text_surface, text_rect)
        
        # 计算指针角度
        hour_angle = (hour + minute / 60) * math.pi / 6
        minute_angle = (minute + second / 60) * math.pi / 30
        second_angle = second * math.pi / 30
        
        # 绘制时针
        hour_length = clock_radius * 0.5
        hour_x = center_x + hour_length * math.sin(hour_angle)
        hour_y = center_y - hour_length * math.cos(hour_angle)
        pygame.draw.line(screen, CLOCK_STYLES[current_style]["hour_color"],
                        (center_x, center_y), (hour_x, hour_y), 8)
        
        # 绘制分针
        minute_length = clock_radius * 0.7
        minute_x = center_x + minute_length * math.sin(minute_angle)
        minute_y = center_y - minute_length * math.cos(minute_angle)
        pygame.draw.line(screen, CLOCK_STYLES[current_style]["minute_color"],
                        (center_x, center_y), (minute_x, minute_y), 5)
        
        # 绘制秒针
        if show_seconds:
            second_length = clock_radius * 0.8
            second_x = center_x + second_length * math.sin(second_angle)
            second_y = center_y - second_length * math.cos(second_angle)
            pygame.draw.line(screen, CLOCK_STYLES[current_style]["second_color"],
                            (center_x, center_y), (second_x, second_y), 2)
        
        # 绘制时钟中心
        pygame.draw.circle(screen, CLOCK_STYLES[current_style]["second_color"],
                          (center_x, center_y), 8)
        
        # 显示日期
        if show_date:
            date_text = f"{year}年{month}月{day}日"
            date_surface = font.render(date_text, True, CLOCK_STYLES[current_style]["clock_color"])
            date_rect = date_surface.get_rect(center=(center_x, center_y + clock_radius + 40))
            screen.blit(date_surface, date_rect)
        
        # 添加粒子效果
        if particle_enabled:
            # 每帧创建少量粒子
            if random.random() < 0.3:
                color = random.choice([
                    CLOCK_STYLES[current_style]["hour_color"],
                    CLOCK_STYLES[current_style]["minute_color"],
                    CLOCK_STYLES[current_style]["second_color"]
                ])
                particles.append(Particle(center_x, center_y, color, clock_radius * 0.9))
            
            # 更新和绘制所有粒子
            particles = [p for p in particles if p.update()]
            for particle in particles:
                particle.draw(screen)
        
        # 显示信息面板
        if show_info:
            info_text = f"按空格键切换样式 | 当前: {CLOCK_STYLES[current_style]['name']}"
            info_surface = small_font.render(info_text, True, CLOCK_STYLES[current_style]["clock_color"])
            screen.blit(info_surface, (20, 20))
            
            controls_text = "S: 显示/隐藏秒针 | D: 显示/隐藏日期 | I: 显示/隐藏信息 | P: 粒子效果开关 | ESC: 退出"
            controls_surface = small_font.render(controls_text, True, CLOCK_STYLES[current_style]["clock_color"])
            screen.blit(controls_surface, (20, HEIGHT - 40))
        
        # 更新屏幕
        pygame.display.flip()
        
        # 控制帧率
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
