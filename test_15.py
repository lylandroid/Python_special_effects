import pygame
import random
import math
import sys
import appcomm.helper.font_helper as font_helper

# 初始化Pygame
pygame.init()

# 设置中文字体，确保中文能正常显示
pygame.font.init()
try:
    # font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 24)
    font = font_helper.FontHelper(None,None,24)
except:
    font = pygame.font.Font(None, 24)  # 如果找不到中文字体，使用默认字体

# 屏幕设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("鼠标发光轨迹特效")

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 轨迹粒子类
class Particle:
    def __init__(self, x, y):
        # 粒子位置和速度
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        
        # 粒子大小和颜色
        self.size = random.randint(5, 15)
        self.alpha = 255  # 透明度
        
        # 随机选择一种颜色
        color_type = random.choice(["彩虹", "蓝色", "紫色", "绿色", "黄色"])
        if color_type == "彩虹":
            self.color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))
        elif color_type == "蓝色":
            self.color = (random.randint(100, 255), random.randint(100, 200), 255)
        elif color_type == "紫色":
            self.color = (random.randint(150, 255), random.randint(100, 200), random.randint(200, 255))
        elif color_type == "绿色":
            self.color = (random.randint(100, 200), random.randint(200, 255), random.randint(100, 200))
        elif color_type == "黄色":
            self.color = (255, random.randint(200, 255), random.randint(100, 200))
        
        # 创建粒子表面并设置颜色和透明度
        self.surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, self.color, (self.size, self.size), self.size)
        
        # 发光效果 - 创建一个更大的半透明光晕
        self.glow_surface = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
        for i in range(10):
            radius = self.size * 2 - i * 2
            alpha = 100 - i * 10
            pygame.draw.circle(self.glow_surface, (*self.color[:3], alpha), (self.size * 2, self.size * 2), radius)

    def update(self):
        # 更新粒子位置
        self.x += self.vx
        self.y += self.vy
        
        # 粒子随时间逐渐消失
        self.alpha -= 3
        if self.alpha <= 0:
            return False  # 返回False表示粒子应该被删除
            
        # 更新表面的透明度
        self.surface.set_alpha(self.alpha)
        self.glow_surface.set_alpha(self.alpha // 2)  # 光晕透明度更低
        
        return True  # 返回True表示粒子仍然存在

    def draw(self, surface):
        # 绘制光晕和粒子
        surface.blit(self.glow_surface, (self.x - self.size * 2, self.y - self.size * 2))
        surface.blit(self.surface, (self.x - self.size, self.y - self.size))

# 主程序
def main():
    clock = pygame.time.Clock()
    particles = []  # 存储所有粒子
    show_info = True  # 是否显示信息文本
    
    # 特效模式: 0=随机颜色, 1=跟随鼠标颜色, 2=彩虹渐变
    effect_mode = 0
    modes = ["随机颜色", "跟随鼠标颜色", "彩虹渐变"]
    
    # 鼠标颜色变量
    mouse_color = (255, 255, 255)
    
    # 彩虹渐变角度
    rainbow_angle = 0
    
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_i:  # 按I键切换信息显示
                    show_info = not show_info
                elif event.key == pygame.K_m:  # 按M键切换特效模式
                    effect_mode = (effect_mode + 1) % 3
        
        # 获取鼠标位置
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # 根据不同特效模式创建粒子
        if effect_mode == 0:  # 随机颜色
            # 每隔几帧创建一个新粒子
            if random.random() < 0.5:
                particles.append(Particle(mouse_x, mouse_y))
        elif effect_mode == 1:  # 跟随鼠标颜色
            # 鼠标颜色随时间变化
            mouse_color = (
                (math.sin(pygame.time.get_ticks() / 1000) * 75 + 180) % 255,
                (math.cos(pygame.time.get_ticks() / 1200) * 75 + 180) % 255,
                (math.sin(pygame.time.get_ticks() / 1500) * 75 + 180) % 255
            )
            
            # 创建粒子
            if random.random() < 0.5:
                p = Particle(mouse_x, mouse_y)
                p.color = mouse_color
                p.surface.fill((0, 0, 0, 0))
                pygame.draw.circle(p.surface, p.color, (p.size, p.size), p.size)
                p.glow_surface.fill((0, 0, 0, 0))
                for i in range(10):
                    radius = p.size * 2 - i * 2
                    alpha = 100 - i * 10
                    pygame.draw.circle(p.glow_surface, (*p.color[:3], alpha), (p.size * 2, p.size * 2), radius)
                particles.append(p)
        elif effect_mode == 2:  # 彩虹渐变
            # 彩虹颜色计算
            rainbow_angle += 0.05
            r = (math.sin(rainbow_angle) * 127 + 128)
            g = (math.sin(rainbow_angle + 2) * 127 + 128)
            b = (math.sin(rainbow_angle + 4) * 127 + 128)
            
            # 创建粒子
            if random.random() < 0.5:
                p = Particle(mouse_x, mouse_y)
                p.color = (int(r), int(g), int(b))
                p.surface.fill((0, 0, 0, 0))
                pygame.draw.circle(p.surface, p.color, (p.size, p.size), p.size)
                p.glow_surface.fill((0, 0, 0, 0))
                for i in range(10):
                    radius = p.size * 2 - i * 2
                    alpha = 100 - i * 10
                    pygame.draw.circle(p.glow_surface, (*p.color[:3], alpha), (p.size * 2, p.size * 2), radius)
                particles.append(p)
        
        # 更新粒子
        particles = [p for p in particles if p.update()]
        
        # 清屏
        screen.fill(BLACK)
        
        # 绘制所有粒子
        for particle in particles:
            particle.draw(screen)
        
        # 显示信息
        if show_info:
            font.render(f"按M键切换模式: {modes[effect_mode]} | 按I键隐藏/显示信息", WHITE)
            font.blit(screen, (10, 10))
            
            font.render(f"粒子数量: {len(particles)}", WHITE)
            font.blit(screen, (10, 40))
            
            font.render("移动鼠标创建轨迹 | 按ESC退出", WHITE)
            font.blit(screen, (10, HEIGHT - 40))
        
        # 更新屏幕
        pygame.display.flip()
        
        # 控制帧率
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
