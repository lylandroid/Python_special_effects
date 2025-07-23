import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.animation import FuncAnimation

# 设置 Matplotlib 支持中文
# 设置 Matplotlib 支持中文，使用可用字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'Noto Sans CJK SC', 'Arial Unicode MS', 'sans-serif']  # 优先尝试多种字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置随机种子，确保每次运行结果可复现
np.random.seed(42)

# 初始化数据
hours = np.arange(0, 24, 1)  # 模拟一天24小时
temperatures = [20 + 5 * np.sin(i / 4) + np.random.normal(0, 1) for i in range(24)]  # 模拟温度数据

def update_temperature(frame):
    """
    更新动画的每一帧
    frame: 当前帧数，用于模拟时间推进
    """
    # 清空当前图形
    ax.clear()
    
    # 更新温度数据（模拟热浪变化）
    new_temp = temperatures[frame % 24] + np.random.normal(0, 0.5)  # 轻微随机扰动
    temperatures.append(new_temp)
    temperatures.pop(0)  # 移除最早的数据，保持列表长度
    
    # 计算颜色：温度越高，颜色越红
    temp_normalized = (new_temp - 15) / (35 - 15)  # 归一化温度到[0,1]
    color = plt.cm.hot(temp_normalized)  # 使用热力图颜色映射
    
    # 绘制折线图
    ax.plot(hours, temperatures, color=color, linewidth=2, marker='o')
    
    # 设置标题和标签
    ax.set_title('热浪来袭 - 实时温度变化', fontsize=14, pad=10)
    ax.set_xlabel('时间 (小时)', fontsize=12)
    ax.set_ylabel('温度 (°C)', fontsize=12)
    
    # 设置坐标轴范围
    ax.set_xlim(0, 23)
    ax.set_ylim(15, 35)
    
    # 添加网格
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 添加当前温度标签
    ax.text(0.02, 0.95, f'当前温度: {new_temp:.1f}°C', transform=ax.transAxes, 
            fontsize=10, color=color, bbox=dict(facecolor='white', alpha=0.8))

# 主函数：设置和运行动画
def run_temperature_animation():
    """
    运行温度变化的动态图表
    """
    global ax  # 声明全局变量，用于动画更新
    fig, ax = plt.subplots(figsize=(10, 6))  # 创建图形窗口，大小10x6
    fig.canvas.manager.set_window_title("实时温度变化")
    # 设置动画
    ani = FuncAnimation(fig, update_temperature, frames=range(100), interval=200)  # 每200ms更新一次
    
    print("欢迎体验热浪来袭动画！关闭窗口退出")
    plt.show()

# 运行程序
run_temperature_animation()