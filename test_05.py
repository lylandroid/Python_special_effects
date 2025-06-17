from PIL import Image  # 用于处理图像
import tkinter as tk   # 用于创建 GUI 窗口
from tkinter import filedialog  # 用于文件选择对话框

def image_to_ascii(image_path, output_width=68):
    """
    将图像转换为彩色 ASCII 艺术
    
    :param image_path: 图像文件的路径
    :param output_width: 输出 ASCII 艺术的宽度（字符数）
    :return: 包含彩色 ASCII 艺术的列表或错误消息
    """
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        return "错误：找不到图像文件！"

    # 获取图像的原始尺寸
    width, height = image.size
    # 计算输出高度，保持图像的比例（字符高度通常是宽度的两倍，所以除以 2）
    aspect_ratio = height / width
    output_height = int(output_width * aspect_ratio / 2)

    # 调整图像大小到指定的宽度和高度
    image = image.resize((output_width, output_height))
    # 将图像转换为灰度模式（亮度值从 0 到 255）
    image = image.convert("L")

    # 定义 ASCII 字符集，从暗到亮排列
    ascii_chars = "@%#*+=-:. "

    # 创建一个列表来存储每一行的 ASCII 艺术
    ascii_art = []

    # 遍历图像的每个像素
    for y in range(output_height):
        line_blocks = []
        current_color = None
        current_text = ""
        for x in range(output_width):
            # 获取像素的亮度值（0-255）
            brightness = image.getpixel((x, y))
            # 根据亮度选择 ASCII 字符
            char_index = int(brightness / 255 * (len(ascii_chars) - 1))
            char = ascii_chars[char_index]
            
            # 根据亮度选择颜色标签
            if brightness < 85:
                color = "dark"
            elif brightness < 170:
                color = "medium"
            else:
                color = "light"
            
            # 如果颜色改变，结束当前的文本块
            if color != current_color:
                if current_text:
                    line_blocks.append((current_text, current_color))
                current_text = char
                current_color = color
            else:
                current_text += char
        
        # 添加最后一段文本块
        if current_text:
            line_blocks.append((current_text, current_color))
        ascii_art.append(line_blocks)

    return ascii_art

# 创建 GUI 窗口
root = tk.Tk()
root.configure(bg="#FFEBCD") 
root.title("彩色 ASCII 艺术")

# 创建一个 Text 组件来显示 ASCII 艺术
text = tk.Text(root, width=100, height=30, font=("Courier", 10))
text.pack()

# 配置颜色标签
text.tag_config("dark", foreground="gray")
text.tag_config("medium", foreground="Orange")
text.tag_config("light", foreground="Gainsboro")
# text.tag_config("light", foreground="white")

def load_image():
    # 打开文件选择对话框
    image_path = filedialog.askopenfilename()
    if image_path:
        # 生成 ASCII 艺术
        ascii_art = image_to_ascii(image_path)
        if isinstance(ascii_art, str):
            # 如果返回的是错误消息，显示错误消息
            text.delete("1.0", "end")
            text.insert("end", ascii_art)
        else:
            # 清空 Text 组件
            text.delete("1.0", "end")
            # 插入 ASCII 艺术
            for line in ascii_art:
                for text_block, color in line:
                    text.insert("end", text_block, color)
                text.insert("end", "\n")

# 创建一个按钮，用于选择图像文件
button = tk.Button(root, text="选择图像", command=load_image)
button.pack()

# 运行 GUI 主循环
root.mainloop()