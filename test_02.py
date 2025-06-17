# import turtle
# import colorsys
# import time

# # 设置中文字体支持
# try:
#     # 尝试注册中文字体
#     turtle.register_font("simhei.ttf")
#     font_name = "SimHei"
# except:
#     # 若注册失败，使用系统默认支持的中文字体
#     font_name = "Arial Unicode MS"  # macOS/Linux可能支持
#     # 或者使用系统默认字体（可能无法正确显示中文）
#     # font_name = "Arial"

# # 创建画布和画笔
# screen = turtle.Screen()
# screen.title("彩虹文字特效")
# screen.bgcolor("black")
# screen.setup(width=800, height=400)

# pen = turtle.Turtle()
# pen.speed(0)
# pen.penup()
# pen.hideturtle()

# # 文字内容和设置
# text = "彩虹文字特效"
# font_size = 40
# font_style = "bold"

# # 彩虹颜色生成函数
# def get_rainbow_color(hue):
#     # 将色调值(0-1)转换为RGB颜色
#     r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
#     return (r, g, b)

# # 绘制彩虹文字
# def draw_rainbow_text(text, x, y, font_size, font_name, font_style, hue_offset=0):
#     pen.penup()
#     pen.goto(x, y)
#     pen.pendown()
    
#     # 逐个字符绘制，每个字符使用不同的颜色
#     for i, char in enumerate(text):
#         # 计算当前字符的色调值
#         hue = (time.time() * 0.3 + i * 0.1 + hue_offset) % 1.0
#         color = get_rainbow_color(hue)
        
#         # 设置画笔颜色并绘制字符
#         pen.color(color)
#         pen.write(char, font=(font_name, font_size, font_style))
        
#         # 移动到下一个字符位置
#         pen.penup()
#         font_space = 0.9
#         if '\u4e00' <= char <= '\u9fff':
#             font_space = 1.4
#         pen.forward(font_size * font_space)  # 字符间距

# # 主循环
# while True:
#     # 清除之前的文字
#     pen.clear()
    
#     # 绘制主文字
#     draw_rainbow_text(text, -200, 0, font_size, font_name, font_style)
    
#     # 绘制副标题
#     draw_rainbow_text("Python Turtle 演示", -180, -80, 24, font_name, "normal", 0.5)
    
#     # 更新屏幕
#     screen.update()
    
#     # 控制动画速度
#     time.sleep(0.03)    


import pygame
import math
import colorsys
import appcomm.helper.font_helper as font_helper

# 初始化
pygame.init()
width, height = 800, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("彩虹文字 - Python 编程")
clock = pygame.time.Clock()

# 字体设置
font_size = 60
# font = pygame.font.SysFont("arial", font_size, bold=True)
font = font_helper.FontHelper(None, None, font_size)

text = "你好，彩虹编程！"

def rainbow_color(index, total, offset):
    """根据字母索引和偏移生成彩虹颜色"""
    hue = (index / total + offset) % 1.0  # 0~1
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    return int(r * 255), int(g * 255), int(b * 255)

offset = 0.0
running = True
while running:
    screen.fill((30, 30, 30))  # 深色背景
    total_chars = len(text)
    x = 50
    y = height // 2 - font_size // 2

    for i, char in enumerate(text):
        color = rainbow_color(i, total_chars, offset)
        rect = font.render(char, color)
        rect.center = (x, y)
        font.blit(screen)
        x += rect.width

    offset += 0.01  # 控制彩虹流动速度
    if offset > 1:
        offset -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
