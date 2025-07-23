import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time

# 设置 Matplotlib 支持中文，使用常见的中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'Noto Sans CJK SC', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置随机种子，确保每次运行结果可复现
np.random.seed(42)

# 模拟人口数据：年龄段、男性人口、女性人口（单位：百万）
age_groups = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70+']
# 模拟2000年到2020年的数据，每年男女人口略有变化
years = list(range(2000, 2021))
# 基础人口数据，添加随机扰动
base_male = [8.5, 7.8, 7.0, 6.5, 5.8, 4.5, 3.0, 2.0]
base_female = [8.0, 7.5, 6.8, 6.3, 5.5, 4.3, 3.2, 2.5]
male_populations = [
    [base + np.random.normal(0, 0.2) for base in base_male]
    for _ in years
]
female_populations = [
    [base + np.random.normal(0, 0.2) for base in base_female]
    for _ in years
]

def update_pyramid(frame):
    """
    更新动画的每一帧，展示某一年的人口金字塔
    frame: 当前帧数，对应年份索引
    """
    # 清空当前图形
    ax.clear()
    
    # 获取当前年份的数据
    year = years[frame % len(years)]
    male_data = male_populations[frame % len(years)]
    female_data = female_populations[frame % len(years)]
    
    # 计算颜色：随年份变化颜色渐变
    color_index = frame / len(years)
    male_color = plt.cm.Blues(color_index)  # 男性使用蓝色渐变
    female_color = plt.cm.Reds(color_index)  # 女性使用红色渐变
    
    # 绘制男性人口（左侧，负值表示）
    ax.barh(age_groups, [-x for x in male_data], color=male_color, label='男性', height=0.4, align='center')
    
    # 绘制女性人口（右侧）
    ax.barh(age_groups, female_data, color=female_color, label='女性', height=0.4, align='center')
    
    # 设置标题和标签
    ax.set_title(f'人口金字塔 - {year}年', fontsize=14, pad=10)
    ax.set_xlabel('人口 (百万)', fontsize=12)
    ax.set_ylabel('年龄段', fontsize=12)
    
    # 设置X轴范围，左右对称
    max_pop = max(max(max(male_data), max(female_data)), 10)
    ax.set_xlim(-max_pop, max_pop)
    
    # 添加网格
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 添加图例
    ax.legend(loc='upper right')
    
    # 添加年份标签
    ax.text(0.02, 0.95, f'年份: {year}', transform=ax.transAxes, fontsize=10, 
            color='black', bbox=dict(facecolor='white', alpha=0.8))

# 主函数：设置和运行动画
def run_population_pyramid():
    """
    运行人口金字塔的动态图表
    """
    global ax  # 声明全局变量，用于动画更新
    fig, ax = plt.subplots(figsize=(10, 6))  # 创建图形窗口，大小10x6
    
    # 设置动画，每500ms更新一次，展示不同年份
    ani = FuncAnimation(fig, update_pyramid, frames=range(len(years)), interval=500)
    
    print("欢迎体验人口金字塔动画！关闭窗口退出")
    plt.show()

# 运行程序
run_population_pyramid()