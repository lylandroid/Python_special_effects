import pygame
import random
import math
import sys
import appcomm.helper.font_helper as font_helper

# 初始化pygame
pygame.init()

# 设置窗口尺寸和标题
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("渐变光辉 - 视觉特效创意画布")

# 确保中文能正常显示
pygame.font.init()
font_options = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC", "Arial Unicode MS"]
# font = None
# for font_name in font_options:
#     try:
#         font = pygame.font.SysFont(font_name, 24)
#         if font.render("测试", True, (255, 255, 255)).get_width() > 10:
#             break
#     except:
#         continue
# if font is None:
#     font = pygame.font.SysFont(None, 24)  # 使用默认字体
font = font_helper.FontHelper(None, None, 24)

# 颜色渐变函数 - 从start_color平滑过渡到end_color
def color_gradient(start_color, end_color, step, total_steps):
    r = start_color[0] + (end_color[0] - start_color[0]) * step / total_steps
    g = start_color[1] + (end_color[1] - start_color[1]) * step / total_steps
    b = start_color[2] + (end_color[2] - start_color[2]) * step / total_steps
    return (int(r), int(g), int(b))

# 绘制粒子效果
def draw_particles(screen, particles, color):
    for particle in particles:
        x, y, size, speed_x, speed_y = particle
        pygame.draw.circle(screen, color, (int(x), int(y)), size)
        
        # 更新粒子位置
        particle[0] += speed_x
        particle[1] += speed_y
        
        # 随机改变粒子大小和速度，增加动态效果
        if random.random() < 0.05:
            particle[2] = max(1, particle[2] + random.randint(-1, 1))
        if random.random() < 0.02:
            particle[3] += random.uniform(-0.1, 0.1)
            particle[4] += random.uniform(-0.1, 0.1)

# 绘制波浪效果
def draw_wave(screen, x, y, amplitude, frequency, color, segments=50):
    points = []
    for i in range(segments + 1):
        wave_x = x + (i * width / segments)
        wave_y = y + math.sin(i * frequency + pygame.time.get_ticks() * 0.001) * amplitude
        points.append((wave_x, wave_y))
    
    pygame.draw.lines(screen, color, False, points, 2)

# 主循环
def main():
    clock = pygame.time.Clock()
    running = True
    
    # 背景渐变参数
    bg_color1 = (20, 20, 40)    # 深蓝紫色
    bg_color2 = (10, 60, 100)   # 深蓝色
    bg_step = 0
    bg_total_steps = 300
    
    # 粒子效果参数
    particles = []
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 3)
        speed_x = random.uniform(-1, 1)
        speed_y = random.uniform(-1, 1)
        particles.append([x, y, size, speed_x, speed_y])
    
    # 波浪效果参数
    waves = []
    for _ in range(3):
        y = random.randint(height // 4, height * 3 // 4)
        amplitude = random.randint(30, 80)
        frequency = random.uniform(0.05, 0.15)
        waves.append((y, amplitude, frequency))
    
    # 特效类型：0-正常，1-烟花，2-彩虹，3-漩涡
    effect_type = 0
    
    # 屏幕抖动效果
    shake_intensity = 0
    shake_x = 0
    shake_y = 0
    
    # 提示文本
    instruction_text = [
        "按空格键切换特效模式",
        "点击鼠标添加粒子",
        "按ESC键退出",
        "按R键重置"
    ]
    
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    effect_type = (effect_type + 1) % 4
                    shake_intensity = 10  # 切换特效时添加震动效果
                elif event.key == pygame.K_r:
                    # 重置所有效果
                    particles.clear()
                    for _ in range(100):
                        x = random.randint(0, width)
                        y = random.randint(0, height)
                        size = random.randint(1, 3)
                        speed_x = random.uniform(-1, 1)
                        speed_y = random.uniform(-1, 1)
                        particles.append([x, y, size, speed_x, speed_y])
                    shake_intensity = 15  # 重置时添加更强的震动效果
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 点击添加粒子
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for _ in range(20):
                    size = random.randint(1, 5)
                    speed = random.uniform(1, 5)
                    angle = random.uniform(0, 2 * math.pi)
                    speed_x = math.cos(angle) * speed
                    speed_y = math.sin(angle) * speed
                    particles.append([mouse_x, mouse_y, size, speed_x, speed_y])
                shake_intensity = 5  # 点击时添加轻微震动
        
        # 更新背景渐变
        bg_step = (bg_step + 1) % bg_total_steps
        
        # 应用屏幕抖动
        if shake_intensity > 0:
            shake_x = random.randint(-shake_intensity, shake_intensity)
            shake_y = random.randint(-shake_intensity, shake_intensity)
            shake_intensity -= 0.5
        else:
            shake_x = 0
            shake_y = 0
        
        # 清屏并绘制背景
        if effect_type == 0:  # 正常渐变
            bg_color = color_gradient(bg_color1, bg_color2, bg_step, bg_total_steps)
            screen.fill(bg_color)
        elif effect_type == 1:  # 烟花效果
            screen.fill((0, 0, 10))  # 深蓝色背景
        elif effect_type == 2:  # 彩虹效果
            for i in range(height):
                hue = (i / height * 360 + pygame.time.get_ticks() * 0.05) % 360
                r, g, b = pygame.Color(0)
                r, g, b = pygame.Color(hue, 100, 100, 100).hsva_to_rgb()
                pygame.draw.line(screen, (r, g, b), (0, i), (width, i))
        elif effect_type == 3:  # 漩涡效果
            screen.fill((0, 0, 0))
            center_x, center_y = width // 2, height // 2
            for i in range(1, 200):
                angle = pygame.time.get_ticks() * 0.001 + i * 0.1
                distance = i * 2 + math.sin(pygame.time.get_ticks() * 0.002 + i * 0.5) * 50
                x = center_x + math.cos(angle) * distance
                y = center_y + math.sin(angle) * distance
                hue = (angle * 180 / math.pi) % 360
                r, g, b = pygame.Color(0)
                r, g, b = pygame.Color(hue, 100, 100, 100).hsva_to_rgb()
                size = max(1, 3 - i * 0.01)
                pygame.draw.circle(screen, (r, g, b), (int(x), int(y)), int(size))
        
        # 绘制波浪
        for y, amplitude, frequency in waves:
            if effect_type == 0 or effect_type == 1:
                # 正常和烟花模式使用渐变颜色
                wave_color = color_gradient(
                    (50, 150, 255), 
                    (150, 50, 255), 
                    (y + pygame.time.get_ticks() * 0.05) % 100, 
                    100
                )
            elif effect_type == 2:
                # 彩虹模式使用基于位置的颜色
                hue = (y / height * 360 + pygame.time.get_ticks() * 0.03) % 360
                r, g, b = pygame.Color(0)
                r, g, b = pygame.Color(hue, 100, 100, 100).hsva_to_rgb()
                wave_color = (r, g, b)
            else:
                # 漩涡模式使用白色
                wave_color = (255, 255, 255)
            
            draw_wave(screen, shake_x, y + shake_y, amplitude, frequency, wave_color)
        
        # 绘制粒子
        for i in range(len(particles) - 1, -1, -1):
            particle = particles[i]
            x, y = particle[0], particle[1]
            
            # 移除屏幕外的粒子
            if x < -100 or x > width + 100 or y < -100 or y > height + 100:
                particles.pop(i)
                continue
            
            # 根据特效类型设置粒子颜色
            if effect_type == 0:  # 正常渐变
                particle_color = color_gradient(
                    (100, 100, 255), 
                    (255, 100, 255), 
                    (x + y + pygame.time.get_ticks() * 0.01) % 100, 
                    100
                )
            elif effect_type == 1:  # 烟花效果
                # 烟花爆炸效果
                if particle[4] > 0:  # 上升阶段
                    particle_color = (255, 255, 200)  # 黄色
                else:  # 爆炸阶段
                    hue = (x / width * 360 + pygame.time.get_ticks() * 0.02) % 360
                    r, g, b = pygame.Color(0)
                    r, g, b = pygame.Color(hue, 100, 100, 100).hsva_to_rgb()
                    particle_color = (r, g, b)
            elif effect_type == 2:  # 彩虹效果
                hue = (x / width * 360 + pygame.time.get_ticks() * 0.05) % 360
                r, g, b = pygame.Color(0)
                r, g, b = pygame.Color(hue, 100, 100, 100).hsva_to_rgb()
                particle_color = (r, g, b)
            else:  # 漩涡效果
                distance_to_center = math.sqrt(
                    (x - width // 2) ** 2 + (y - height // 2) ** 2
                )
                hue = (distance_to_center / 10 + pygame.time.get_ticks() * 0.03) % 360
                r, g, b = pygame.Color(0)
                r, g, b = pygame.Color(hue, 100, 100, 100).hsva_to_rgb()
                particle_color = (r, g, b)
            
            # 绘制粒子
            pygame.draw.circle(
                screen, 
                particle_color, 
                (int(x + shake_x), int(y + shake_y)), 
                particle[2]
            )
            
            # 烟花效果特殊处理
            if effect_type == 1:
                # 上升阶段
                if particle[4] > 0:
                    particle[4] -= 0.05  # 减速上升
                    if particle[4] <= 0:  # 到达最高点，爆炸成多个粒子
                        x, y, size = particle[0], particle[1], particle[2]
                        particles.pop(i)  # 移除原粒子
                        # 添加爆炸粒子
                        for _ in range(30):
                            explode_size = random.randint(1, 3)
                            speed = random.uniform(0.5, 3)
                            angle = random.uniform(0, 2 * math.pi)
                            speed_x = math.cos(angle) * speed
                            speed_y = math.sin(angle) * speed
                            particles.append([x, y, explode_size, speed_x, speed_y])
                # 爆炸后粒子逐渐消失
                else:
                    particle[2] = max(0, particle[2] - 0.05)
                    if particle[2] <= 0:
                        particles.pop(i)
        
        # 添加新粒子，保持总数量
        while len(particles) < 100 and effect_type != 1:  # 烟花模式不自动添加粒子
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(1, 3)
            speed_x = random.uniform(-1, 1)
            speed_y = random.uniform(-1, 1)
            particles.append([x, y, size, speed_x, speed_y])
        
        # 显示特效模式
        effect_names = ["渐变模式", "烟花模式", "彩虹模式", "漩涡模式"]
        font.render(f"特效: {effect_names[effect_type]}", (255, 255, 255))
        font.blit(screen, (10, 10))
        
        # 显示提示
        for i, text in enumerate(instruction_text):
            font.render(text, (255, 255, 255))
            font.blit(screen, (10, height - 30 * (len(instruction_text) - i)))
    
        
        # 更新显示
        pygame.display.flip()
        
        # 控制帧率
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()