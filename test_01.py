import pygame
import random
import math
import appcomm.helper.font_helper as font_helper

# 初始化pygame
pygame.init()

# 设置窗口尺寸和标题
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("闪烁星空")

# 确保中文能正常显示
# pygame.font.init()
font_options = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC", "Arial Unicode MS"]

font = font_helper.FontHelper(None,None,24)

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 200)
BLUE = (135, 206, 235)
RED = (255, 100, 100)
GREEN = (100, 255, 100)

class Star:
    """星星类，代表夜空中的一颗星星"""
    
    def __init__(self):
        # 星星的位置
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        
        # 星星的属性
        self.size = random.uniform(0.5, 3)  # 星星大小
        self.base_brightness = random.randint(100, 255)  # 基础亮度
        self.brightness = self.base_brightness  # 当前亮度
        self.frequency = random.uniform(0.01, 0.05)  # 闪烁频率
        self.phase = random.uniform(0, 2 * math.pi)  # 闪烁相位
        self.color = random.choice([WHITE, YELLOW, BLUE, RED, GREEN])  # 星星颜色
        self.speed = random.uniform(0.01, 0.1)  # 移动速度
        self.direction = random.uniform(0, 2 * math.pi)  # 移动方向
        
        # 流星属性
        self.is_meteor = False
        self.meteor_trail = []  # 流星尾迹
        self.meteor_length = 20  # 流星尾迹长度
        self.meteor_speed = 5  # 流星速度
        self.meteor_timer = random.randint(300, 1000)  # 流星出现倒计时
    
    def update(self):
        """更新星星状态"""
        # 倒计时流星出现
        if self.meteor_timer > 0:
            self.meteor_timer -= 1
        elif not self.is_meteor and random.random() < 0.0001:  # 极小概率触发流星
            self.is_meteor = True
            self.meteor_trail = [(self.x, self.y)] * self.meteor_length
        
        if self.is_meteor:
            # 更新流星位置
            self.x += math.cos(self.direction) * self.meteor_speed
            self.y += math.sin(self.direction) * self.meteor_speed
            self.meteor_trail.insert(0, (self.x, self.y))
            self.meteor_trail.pop()
            
            # 流星移出屏幕或尾迹消失后重置
            if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
                self.reset()
        else:
            # 普通星星闪烁效果
            time = pygame.time.get_ticks() * 0.001  # 转换为秒
            self.brightness = int(self.base_brightness + 
                                 30 * math.sin(time * self.frequency + self.phase))
            self.brightness = max(50, min(255, self.brightness))  # 限制亮度范围
            
            # 轻微移动
            self.x += math.cos(self.direction) * self.speed
            self.y += math.sin(self.direction) * self.speed
            
            # 边界检查
            if self.x < 0:
                self.x = WIDTH
            elif self.x > WIDTH:
                self.x = 0
            if self.y < 0:
                self.y = HEIGHT
            elif self.y > HEIGHT:
                self.y = 0
    
    def reset(self):
        """重置星星状态"""
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.uniform(0.5, 3)
        self.base_brightness = random.randint(100, 255)
        self.frequency = random.uniform(0.01, 0.05)
        self.phase = random.uniform(0, 2 * math.pi)
        self.color = random.choice([WHITE, YELLOW, BLUE, RED, GREEN])
        self.speed = random.uniform(0.01, 0.1)
        self.direction = random.uniform(0, 2 * math.pi)
        self.is_meteor = False
        self.meteor_trail = []
        self.meteor_timer = random.randint(300, 1000)
    
    def draw(self, surface):
        """绘制星星"""
        if self.is_meteor:
            # 绘制流星
            for i, (tx, ty) in enumerate(self.meteor_trail):
                alpha = 255 - (i * 255 // self.meteor_length)
                size = self.size - (i * self.size // self.meteor_length)
                if alpha > 0 and size > 0:
                    color = (min(self.color[0], alpha), 
                             min(self.color[1], alpha), 
                             min(self.color[2], alpha))
                    pygame.draw.circle(surface, color, (int(tx), int(ty)), max(1, int(size)))
        else:
            # 绘制普通星星
            # 基础圆形
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))
            
            # 亮度效果 - 外圈光晕
            if self.brightness > 200:
                glow_size = self.size + 1
                glow_color = (self.color[0], self.color[1], self.color[2], 
                             int((self.brightness - 200) * 2.5))
                pygame.draw.circle(surface, glow_color, (int(self.x), int(self.y)), 
                                  int(glow_size))
            
            # 特殊星星 - 十字星效果
            if self.size > 2 and random.random() < 0.3:
                cross_size = self.size * 0.7
                pygame.draw.line(surface, self.color, 
                                (int(self.x - cross_size), int(self.y)), 
                                (int(self.x + cross_size), int(self.y)), 1)
                pygame.draw.line(surface, self.color, 
                                (int(self.x), int(self.y - cross_size)), 
                                (int(self.x), int(self.y + cross_size)), 1)

def main():
    """主函数"""
    clock = pygame.time.Clock()
    stars = [Star() for _ in range(200)]  # 创建200颗星星
    running = True
    
    # 创建渐变背景
    background = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        # 从上到下的深蓝色渐变
        blue_value = int(10 + (y / HEIGHT) * 40)
        pygame.draw.line(background, (0, 0, blue_value), (0, y), (WIDTH, y))
    
    # 显示说明文字
    instructions_rect = font.render("按ESC键退出，空格键添加流星", WHITE)
    instructions_rect.bottomright = (WIDTH - 20, HEIGHT - 20)
    
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # 空格键添加流星
                    for _ in range(5):
                        star = random.choice(stars)
                        star.is_meteor = True
                        star.meteor_trail = [(star.x, star.y)] * star.meteor_length
                        star.direction = random.uniform(0, 2 * math.pi)
        
        # 清屏
        screen.blit(background, (0, 0))
        
        # 更新和绘制星星
        for star in stars:
            star.update()
            star.draw(screen)
        
        # 显示说明文字
        font.blit(screen)
        # screen.blit(instructions, instructions_rect)
        
        # 刷新屏幕
        pygame.display.flip()
        
        # 控制帧率
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()    