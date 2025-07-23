# 导入 matplotlib.pyplot，它是我们的“首席画家”，我们给它起个小名叫 plt
import matplotlib.pyplot as plt
# 导入 matplotlib.animation，它是我们的“动画导演”，负责让画面动起来
import matplotlib.animation as animation
# 导入 random 模块，用来生成随机数，模拟股票价格的随机波动
import random
from collections import deque

# --- 1. 初始化我们的“画板”和“数据” ---

# 创建一个新的画板(figure)和一块画布(ax)
# figsize=(10, 6) 设置了画板的大小，让图表看起来更宽敞
fig, ax = plt.subplots(figsize=(10, 6))
fig.canvas.manager.set_window_title("模拟股票实时价格")
# 创建一个“双端队列”(deque)来存放我们的数据
# 我们可以把它想象成一个神奇的管道，当新的数据从右边进来时，旧的数据会从左边出去
# 这样可以保持我们的图表只显示最近一段时间的数据，不会无限变长
# maxlen=50 意味着我们只保留最新的50个数据点
price_data = deque(maxlen=50) 
time_data = deque(maxlen=50)

# 给我们的股票设置一个初始价格
current_price = 100.0

# --- 2. 定义动画的每一“帧”如何更新 ---

# 这个函数是整个动画的核心，它告诉程序每一帧画面应该画什么
# i 是由动画导演(FuncAnimation)自动传入的帧数，我们这里暂时用不到它
def update(i):
    global current_price # 声明我们要修改全局变量 current_price
    
    # --- 模拟价格波动 ---
    # 我们用一个随机数来模拟价格的上涨或下跌
    # random.uniform(-0.5, 1.5) 会生成一个 -0.5 到 1.5 之间的随机小数
    # 因为正数范围更大，所以股票价格整体趋势会是“飙升”的！
    change = random.uniform(-1.5, 1.5)
    current_price += change
    
    # --- 更新我们的数据管道 ---
    # 将新的时间和价格数据添加到管道的右边
    # len(time_data) + 1 代表当前是第几次更新
    time_data.append(len(time_data) + 1)
    price_data.append(current_price)

    # --- 开始绘制 ---
    # 每次更新前，先清空画布，就像擦掉黑板，准备画新的内容
    ax.clear()
    
    # 在我们干净的画布上，画出时间和价格的折线图
    # 'o-' 表示我们希望用圆点标记数据点，并用实线连接它们
    # color='#4CAF50' 是一种充满活力的绿色，代表股票正在上涨！
    ax.plot(time_data, price_data, 'o-', color='#4CAF50', markersize=4)
    
    # --- 美化我们的图表 ---
    # 设置图表的标题，字体加粗，让它看起来更专业
    ax.set_title('模拟股票实时价格 (SOARING!)', fontsize=16, fontweight='bold')
    # 设置X轴和Y轴的标签
    ax.set_xlabel('时间 (秒)', fontsize=12)
    ax.set_ylabel('价格 ($)', fontsize=12)
    # 添加网格线，让数据点更容易看清楚
    ax.grid(True, linestyle='--', alpha=0.6)
    # 让图表的边缘留出一些空白，更好看
    ax.margins(x=0.1, y=0.1) 
    # 给图表加上一个漂亮的背景色
    ax.set_facecolor('#f0f0f0')

# --- 3. 创建并启动动画 ---

# FuncAnimation 是我们的“动画导演”
# 它会做三件事：
# 1. 在哪个画板(fig)上播放动画
# 2. 每一帧调用哪个函数(update)来更新画面
# 3. 每隔多久(interval)更新一次，单位是毫秒 (1000ms = 1秒)
# blit=False 是一个技术参数，对于初学者我们先设为False
ani = animation.FuncAnimation(fig, update, interval=1000)

# plt.show() - 大戏开幕！向全世界展示我们的动态图表
plt.show()