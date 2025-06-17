import pygame
import random
import asyncio
import platform

# 初始化 Pygame，用于创建动画窗口
pygame.init()

# 设置屏幕大小
screen_width = 800  # 窗口宽度
screen_height = 600  # 窗口高度
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Python 数字雨 - 黑客帝国")

# 定义颜色
black = (0, 0, 0)  # 背景颜色：黑色
green = (0, 255, 0)  # 数字颜色：绿色

# 设置字体
try:
    font = pygame.font.SysFont("Courier", 20)  # 使用 Courier 字体，模拟代码风格
except:
    font = pygame.font.Font(None, 20)  # 如果 Courier 不可用，使用默认字体

# 数字流类，管理每一列的字符
class Stream:
    def __init__(self, x):
        self.x = x  # 列的 x 坐标
        self.y = random.randint(-screen_height, 0)  # 随机初始 y 坐标
        self.speed = random.randint(2, 5)  # 随机下落速度
        self.chars = []  # 存储字符的列表
        self.length = random.randint(10, 20)  # 每列字符数量
        for _ in range(self.length):
            char = chr(random.randint(33, 126))  # 随机 ASCII 字符
            alpha = random.randint(50, 255)  # 随机透明度
            self.chars.append((char, alpha))

    def update(self):
        # 向下移动
        self.y += self.speed
        # 如果流超出屏幕底部，重置到顶部
        if self.y > screen_height:
            self.y = -self.length * 20
            self.chars = [(chr(random.randint(33, 126)), random.randint(50, 255)) for _ in range(self.length)]
        # 随机更新字符和透明度
        for i in range(len(self.chars)):
            if random.random() < 0.1:  # 10% 概率更新字符
                self.chars[i] = (chr(random.randint(33, 126)), random.randint(50, 255))

    def draw(self):
        # 绘制每一列的字符
        for i, (char, alpha) in enumerate(self.chars):
            # 计算字符的 y 坐标
            char_y = self.y + i * 20
            if 0 <= char_y <= screen_height:  # 仅绘制屏幕内的字符
                # 创建字符表面，应用透明度
                text = font.render(char, True, (0, min(255, alpha), 0))
                screen.blit(text, (self.x, char_y))

# 创建多列数字流
streams = [Stream(x) for x in range(0, screen_width, 20)]  # 每 20 像素一列

# 初始化设置
def setup():
    pass  # 已经初始化，无需额外设置

# 主更新循环
def update_loop():
    # 处理事件，允许关闭窗口
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if platform.system() != "Emscripten":  # 非 Pyodide 环境
                pygame.quit()
                exit()

    # 清屏，绘制黑色背景
    screen.fill(black)

    # 更新并绘制每列数字流
    for stream in streams:
        stream.update()
        stream.draw()

    # 更新屏幕显示
    pygame.display.flip()

# 设置帧率（每秒帧数）
FPS = 30

# 异步主循环（适配 Pyodide）
async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

# 根据运行环境选择循环模式
if platform.system() == "Emscripten":
    # Pyodide 环境使用异步循环
    asyncio.ensure_future(main())
else:
    # 本地运行使用标准 Pygame 循环
    if __name__ == "__main__":
        setup()
        running = True
        clock = pygame.time.Clock()
        while running:
            update_loop()
            clock.tick(FPS)
        pygame.quit()