import turtle

# 创建画布和画笔
screen = turtle.Screen()
pen = turtle.Turtle()

# 设置画笔速度
pen.speed(0)

# 绘制彩色螺旋线
colors = ['red', 'purple', 'blue', 'green', 'orange', 'yellow']
for x in range(360):
    pen.pencolor(colors[x % 6])
    pen.width(x / 100 + 1)
    pen.forward(x)
    pen.left(59)

# 完成绘制
turtle.done()