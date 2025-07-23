import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time

# 设置 Matplotlib 支持中文，使用 macOS 友好的字体
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Microsoft YaHei', 'Noto Sans CJK SC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置随机种子，确保每次运行结果可复现
np.random.seed(42)

# 模拟数据：5个类别的得分
categories = ['力量', '速度', '智慧', '耐力', '敏捷']
num_categories = len(categories)
num_frames = 50  # 动画帧数
# 初始得分（0-10 分）
scores = [6.0, 7.5, 8.0, 5.5, 6.5]
# 生成动态得分数据，确保每帧有 5 个得分
score_history = [scores.copy()]  # 保存初始得分
for _ in range(num_frames - 1):
    new_scores = [max(0, min(10, s + np.random.uniform(-0.5, 0.5))) for s in score_history[-1]]  # 随机变化
    score_history.append(new_scores)

# 计算雷达图的角度
angles = np.linspace(0, 2 * np.pi, num_categories, endpoint=False).tolist()
angles += angles[:1]  # 闭合雷达图

def update_radar(frame):
    """
    更新动画的每一帧，展示雷达图和扫描线
    frame: 当前帧数，用于控制数据和扫描线角度
    """
    # 清空当前图形
    ax.clear()
    
    # 获取当前帧的得分
    current_scores = score_history[frame]
    # 确保 current_scores 有 5 个元素
    if len(current_scores) != num_categories:
        print(f"Error: current_scores has {len(current_scores)} elements, expected {num_categories}")
        current_scores = current_scores[:num_categories]  # 截断到正确长度
    # 闭合数据以绘制雷达图
    current_scores = current_scores + current_scores[:1]
    
    # 调试：打印数组长度
    print(f"Frame: {frame}, angles: {len(angles)}, scores: {len(current_scores)}")
    
    # 绘制雷达图区域
    ax.fill(angles, current_scores, color=plt.cm.viridis(frame / num_frames), alpha=0.3)
    ax.plot(angles, current_scores, color=plt.cm.viridis(frame / num_frames), linewidth=2)
    
    # 绘制扫描线
    scan_angle = (frame * 0.1) % (2 * np.pi)  # 扫描线每帧旋转 0.1 弧度
    ax.plot([0, scan_angle], [0, 10], color='red', linestyle='--', linewidth=2, alpha=0.8)
    
    # 设置标题和标签
    ax.set_title('雷达扫描 - 多维数据', fontsize=14, pad=20)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12)
    ax.set_ylim(0, 10)  # 得分范围 0-10
    
    # 添加网格
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 设置雷达图样式
    ax.spines['polar'].set_visible(False)  # 隐藏极坐标边框
    ax.set_rlabel_position(0)  # 半径标签位置
    
    # 添加当前帧（时间）标签
    ax.text(0.02, 0.95, f'时间: {frame + 1}', transform=ax.transAxes, fontsize=10, 
            color='black', bbox=dict(facecolor='white', alpha=0.8))

# 主函数：设置和运行动画
def run_radar_scan_animation():
    """
    运行雷达扫描的动态图表
    """
    global ax  # 声明全局变量，用于动画更新
    fig = plt.figure(figsize=(6, 6))  # 创建图形窗口，大小 8x8（适合圆形雷达图）
    ax = fig.add_subplot(111, projection='polar')  # 创建极坐标轴
    
    # 设置动画，每 100ms 更新一次
    ani = FuncAnimation(fig, update_radar, frames=range(num_frames), interval=100)
    
    print("欢迎体验雷达扫描动画！关闭窗口退出")
    plt.show()

# 运行程序
run_radar_scan_animation()