# 导入Matplotlib和NumPy库，用于绘图和数据处理
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import fontManager

# 动态选择支持中文的字体
def find_chinese_font():
    """
    查找系统中支持中文的字体，返回第一个可用的字体名称
    """
    # 常见的支持中文的字体列表
    chinese_fonts = [
        'Microsoft YaHei',  # Windows常用
        'PingFang SC',      # macOS常用
        'Noto Sans CJK',    # 跨平台字体
        'Arial Unicode MS',  # 通用字体
        'SimHei',           # Windows黑体
        'Heiti TC',         # macOS字体
    ]
    
    # 检查系统可用字体
    available_fonts = {f.name for f in fontManager.ttflist}
    for font in chinese_fonts:
        if font in available_fonts:
            return font
    
    # 如果没有找到支持中文的字体，使用默认字体并打印警告
    print("警告：未找到支持中文的字体，中文可能显示为方块。建议安装'Noto Sans CJK'字体。")
    return 'sans-serif'

# 设置Matplotlib支持中文显示，防止乱码
font_name = find_chinese_font()
plt.rcParams['font.sans-serif'] = [font_name]  # 使用动态选择的字体
plt.rcParams['axes.unicode_minus'] = False     # 解决负号显示为方块的问题

def create_waterfall_chart(data, labels, title="瀑布图 - 累积变化追踪"):
    """
    生成瀑布图，展示数据的累积变化，支持中文显示
    参数:
        data: 数值列表，表示每次变化的量（正数为增加，负数为减少）
        labels: 标签列表，对应每个数据的描述（支持中文）
        title: 图表标题（支持中文）
    """
    # 初始化数据
    # 起始值为0，计算每次变化后的累积值
    values = [0] + [sum(data[:i+1]) for i in range(len(data))]
    
    # 创建画布和子图，设置尺寸
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 设置颜色：正数用绿色，负数用红色，起始和结束用蓝色
    colors = ['blue'] + ['green' if x >= 0 else 'red' for x in data] + ['blue']
    
    # 绘制柱状图（瀑布图的每个柱子）
    for i in range(len(data)):
        # 柱子从前一个累积值开始，高度为当前变化量
        ax.bar(i, data[i], bottom=values[i], color=colors[i+1], edgecolor='black')
    
    # 绘制连接线，突出累积变化的趋势
    for i in range(len(values)-1):
        ax.plot([i, i+1], [values[i], values[i]], color='gray', linestyle='--', linewidth=1)
    
    # 添加数据标签，显示每个柱子的值
    for i, (value, change) in enumerate(zip(values, data)):
        if i < len(data):  # 跳过最后一个柱子（总计）
            ax.text(i, values[i] + change/2, f'{change:+.1f}', 
                    ha='center', va='center', color='white', fontsize=10, fontweight='bold')
    
    # 设置x轴标签（支持中文的描述）
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    
    # 设置y轴标签和标题（支持中文）
    ax.set_ylabel('累积值')
    ax.set_title(title, fontsize=14, pad=15)
    
    # 添加网格线，增强可读性
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # 调整布局，防止标签被裁剪
    plt.tight_layout()
    
    # 保存并显示图表
    plt.savefig('waterfall_chart.png', bbox_inches='tight')  # 使用bbox_inches确保中文不被裁剪
    plt.show()
    print("瀑布图已保存为: waterfall_chart.png")

# 示例用法
if __name__ == "__main__":
    # 示例数据：模拟一个月的收支变化
    data = [100, 50, -30, 20, -10, 40]  # 正数表示收入，负数表示支出
    labels = ['起始', '收入1', '支出1', '收入2', '支出2', '收入3', '总计']
    
    # 调用函数生成瀑布图，标题支持中文
    create_waterfall_chart(data, labels, title="月度收支瀑布图")