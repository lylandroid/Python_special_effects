import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time

# 设置 Matplotlib 支持中文，使用常见的中文字体（适合 macOS 和其他系统）
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Microsoft YaHei', 'Noto Sans CJK SC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置随机种子，确保每次运行结果可复现
np.random.seed(42)

# 模拟数据：5个团队的得分
teams = ['团队 A', '团队 B', '团队 C', '团队 D', '团队 E']
scores = [10, 12, 8, 15, 9]  # 初始得分
num_frames = 50  # 动画帧数

# 生成动态得分数据
score_history = [scores.copy()]  # 保存初始得分
for _ in range(num_frames - 1):
    new_scores = [max(0, s + np.random.uniform(-2, 3)) for s in score_history[-1]]  # 随机变化
    score_history.append(new_scores)

def update_bars(frame):
    """
    更新动画的每一帧，展示柱状图的动态变化
    frame: 当前帧数，用于获取对应时间点的得分
    """
    # 清空当前图形
    ax.clear()
    
    # 获取当前帧的得分
    current_scores = score_history[frame]
    
    # 为每个团队分配颜色
    colors = plt.cm.Set2(np.linspace(0, 1, len(teams)))
    
    # 绘制柱状图
    bars = ax.bar(teams, current_scores, color=colors)
    
    # 设置标题和标签
    ax.set_title('柱状竞赛 - 团队得分', fontsize=14, pad=10)
    ax.set_xlabel('团队', fontsize=12)
    ax.set_ylabel('得分', fontsize=12)
    
    # 设置 Y 轴范围，留出空间显示标签
    ax.set_ylim(0, max(max(score_history)) + 5)
    
    # 添加网格
    ax.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    # 在每个柱子上方添加得分标签
    for bar, score in zip(bars, current_scores):
        ax.text(bar.get_x() + bar.get_width() / 2, score + 0.5, f'{score:.1f}', 
                ha='center', va='bottom', fontsize=10)
    
    # 添加当前帧（时间）标签
    ax.text(0.02, 0.95, f'时间: {frame + 1}', transform=ax.transAxes, fontsize=10, 
            color='black', bbox=dict(facecolor='white', alpha=0.8))

# 主函数：设置和运行动画
def run_bar_race_animation():
    """
    运行柱状竞赛的动态图表
    """
    global ax  # 声明全局变量，用于动画更新
    fig, ax = plt.subplots(figsize=(10, 6))  # 创建图形窗口，大小 10x6
    
    # 设置动画，每 200ms 更新一次
    ani = FuncAnimation(fig, update_bars, frames=range(num_frames), interval=200)
    
    print("欢迎体验柱状竞赛动画！关闭窗口退出")
    plt.show()

# 运行程序
run_bar_race_animation()