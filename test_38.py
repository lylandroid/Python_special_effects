import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.animation import FuncAnimation
import time

# 设置 Matplotlib 支持中文，使用 macOS 友好的字体
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Microsoft YaHei', 'Noto Sans CJK SC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置随机种子，确保每次运行结果可复现
np.random.seed(42)

# 模拟数据：10x10 网格的密度数据
grid_size = 10
num_frames = 50  # 动画帧数
# 初始化密度数据（0-100 表示密度）
density = np.random.uniform(0, 100, (grid_size, grid_size))
# 生成动态密度数据
density_history = [density.copy()]
for _ in range(num_frames - 1):
    # 每次帧随机调整密度，模拟变化
    new_density = density_history[-1] + np.random.uniform(-10, 10, (grid_size, grid_size))
    new_density = np.clip(new_density, 0, 100)  # 限制密度在 0-100
    density_history.append(new_density)

has_first = True
def update_heatmap(frame):
    """
    更新动画的每一帧，展示热力图的动态变化
    frame: 当前帧数，用于获取对应时间点的密度数据
    """
    global has_first
    if has_first:
        time.sleep(10)
        has_first = False
    # 清空当前图形
    ax.clear()
    # 获取当前帧的密度数据
    current_density = density_history[frame]
    # 绘制热力图
    sns.heatmap(current_density, ax=ax, cmap='YlOrRd', cbar=True, 
                vmin=0, vmax=100, square=True, 
                cbar_kws={'label': '密度'})

    
    # 设置标题和标签
    ax.set_title('热力网格 - 动态密度', fontsize=14, pad=10)
    ax.set_xlabel('X 坐标', fontsize=12)
    ax.set_ylabel('Y 坐标', fontsize=12)
    
    # 设置坐标轴刻度
    ax.set_xticks(np.arange(0.5, grid_size, 1))
    ax.set_yticks(np.arange(0.5, grid_size, 1))
    ax.set_xticklabels(range(1, grid_size + 1))
    ax.set_yticklabels(range(1, grid_size + 1))
    
    # 添加当前帧（时间）标签
    ax.text(0.02, 0.95, f'时间: {frame + 1}', transform=ax.transAxes, fontsize=10, 
            color='black', bbox=dict(facecolor='white', alpha=0.8))

# 主函数：设置和运行动画
def run_heatmap_animation():
    """
    运行热力网格的动态图表
    """
    global ax  # 声明全局变量，用于动画更新
    fig, ax = plt.subplots(figsize=(8, 8))  # 创建图形窗口，大小 8x8（适合正方形热力图）
    
    # 设置动画，每 200ms 更新一次
    ani = FuncAnimation(fig, update_heatmap, frames=range(num_frames), interval=200)
    
    print("欢迎体验热力网格动画！关闭窗口退出")
    plt.show()

# 运行程序
run_heatmap_animation()