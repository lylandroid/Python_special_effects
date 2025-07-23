import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time

# 设置 Matplotlib 支持中文，使用常见的中文字体
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Microsoft YaHei', 'Noto Sans CJK SC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置随机种子，确保每次运行结果可复现
np.random.seed(42)

# 创建 3D 曲面的网格数据
x = np.linspace(-5, 5, 100)  # 在 x 轴上生成 100 个点，从 -5 到 5
y = np.linspace(-5, 5, 100)  # 在 y 轴上生成 100 个点，从 -5 到 5
X, Y = np.meshgrid(x, y)  # 创建网格，用于 3D 曲面

# 定义曲面高度的函数
def get_surface_height(x, y, t):
    """
    计算 3D 曲面的高度 z，随时间 t 变化
    x, y: 网格坐标
    t: 时间参数，用于动态效果
    """
    r = np.sqrt(x**2 + y**2)  # 计算点到原点的距离
    z = np.sin(r + t)  # 使用正弦函数创建波动效果，t 使曲面随时间变化
    return z

is_bar = False
def update_surface(frame):
    """
    更新动画的每一帧，旋转 3D 曲面
    frame: 当前帧数，用于控制时间和旋转角度
    """
    # 清空当前图形
    ax.clear()
    
    # 计算当前时间点的曲面高度
    t = frame * 0.1  # 时间参数，每次帧增加 0.1
    Z = get_surface_height(X, Y, t)
    
    # 绘制 3D 曲面，使用颜色映射
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
    
    # 设置标题和标签
    ax.set_title('3D 曲面 - 动态旋转', fontsize=14, pad=10)
    ax.set_xlabel('X 轴', fontsize=12)
    ax.set_ylabel('Y 轴', fontsize=12)
    ax.set_zlabel('Z 轴（高度）', fontsize=12)
    
    # 设置视角，随时间旋转
    ax.view_init(elev=30, azim=frame * 4 % 360)  # 绕 Z 轴旋转，每帧旋转 4 度
    
    # 设置 Z 轴范围
    ax.set_zlim(-1.5, 1.5)
    
    # 添加颜色条
    global is_bar
    if not is_bar:  # 只在第一帧添加颜色条，避免重复
        is_bar = True
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='高度')

# 主函数：设置和运行动画
def run_3d_surface_animation():
    """
    运行 3D 曲面动态图表
    """
    global ax, fig  # 声明全局变量，用于动画更新
    fig = plt.figure(figsize=(10, 6))  # 创建图形窗口，大小 10x6
    ax = fig.add_subplot(111, projection='3d')  # 创建 3D 坐标轴
    
    # 设置动画，每 50ms 更新一次
    ani = FuncAnimation(fig, update_surface, frames=range(100), interval=50)
    
    print("欢迎体验 3D 曲面动画！关闭窗口退出")
    plt.show()

# 运行程序
run_3d_surface_animation()