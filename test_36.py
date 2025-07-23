import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time

# 设置 Matplotlib 支持中文，使用 macOS 友好的字体
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Microsoft YaHei', 'Noto Sans CJK SC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置随机种子，确保每次运行结果可复现
np.random.seed(42)

# 模拟气泡数据：位置、大小、颜色
num_bubbles = 20  # 气泡数量
x = np.random.uniform(-10, 10, num_bubbles)  # 气泡的 x 坐标
y = np.random.uniform(-10, 10, num_bubbles)  # 气泡的 y 坐标
sizes = np.random.uniform(50, 200, num_bubbles)  # 气泡初始大小
speeds = np.random.uniform(-0.5, 0.5, (num_bubbles, 2))  # 每个气泡的 x, y 移动速度

def update_bubbles(frame):
    """
    更新动画的每一帧，展示气泡的动态变化
    frame: 当前帧数，用于控制时间和气泡变化
    """
    global x, y, sizes  # 使用全局变量更新气泡状态
    
    # 清空当前图形
    ax.clear()
    
    # 更新气泡位置（模拟移动）
    x += speeds[:, 0]  # 更新 x 坐标
    y += speeds[:, 1]  # 更新 y 坐标
    
    # 更新气泡大小（模拟爆炸：先增大后缩小）
    t = frame % 40  # 循环周期为 40 帧
    if t < 20:
        sizes = sizes * 1.05  # 前 20 帧，气泡大小增加 5%
    else:
        sizes = sizes * 0.95  # 后 20 帧，气泡大小减少 5%
    
    # 限制大小范围，防止过大或过小
    sizes = np.clip(sizes, 20, 1000)
    
    # 使用颜色映射，根据大小设置颜色
    colors = plt.cm.viridis(sizes / 1000)  # 颜色随大小变化
    
    # 绘制气泡（散点图）
    scatter = ax.scatter(x, y, s=sizes, c=colors, alpha=0.6)
    
    # 设置标题和标签
    ax.set_title('气泡爆炸 - 动态展示', fontsize=14, pad=10)
    ax.set_xlabel('X 轴', fontsize=12)
    ax.set_ylabel('Y 轴', fontsize=12)
    
    # 设置坐标轴范围
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    
    # 添加网格
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 添加当前帧（时间）标签
    ax.text(0.02, 0.95, f'时间: {frame + 1}', transform=ax.transAxes, fontsize=10, 
            color='black', bbox=dict(facecolor='white', alpha=0.8))

# 主函数：设置和运行动画
def run_bubble_explosion():
    """
    运行气泡爆炸的动态图表
    """
    global ax  # 声明全局变量，用于动画更新
    fig, ax = plt.subplots(figsize=(10, 6))  # 创建图形窗口，大小 10x6
    
    # 设置动画，每 100ms 更新一次
    ani = FuncAnimation(fig, update_bubbles, frames=range(100), interval=100)
    
    print("欢迎体验气泡爆炸动画！关闭窗口退出")
    plt.show()

# 运行程序
run_bubble_explosion()