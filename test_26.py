from PIL import Image  # 导入Pillow库的Image模块，用于处理图像
import os  # 导入os模块，用于检查文件是否存在

def apply_mosaic_filter(input_path, output_path, block_size=10):
    """
    为图像添加马赛克滤镜效果
    参数:
        input_path: 输入图像的路径
        output_path: 输出图像的路径
        block_size: 马赛克方块的大小（像素），越大越模糊
    """
    # 检查输入图像文件是否存在
    if not os.path.exists(input_path):
        print(f"错误：找不到图像文件 {input_path}！")
        return

    try:
        # 打开图像
        img = Image.open(input_path)
        # 获取图像的宽度和高度
        width, height = img.size
        # 确保图像是RGB模式（如果不是，转换为RGB）
        img = img.convert("RGB")

        # 创建一个新的空白图像，用于存储马赛克效果
        mosaic_img = Image.new("RGB", (width, height))

        # 遍历图像，按block_size大小的方块处理
        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                # 定义当前方块的边界
                box = (x, y, min(x + block_size, width), min(y + block_size, height))
                # 截取当前方块区域
                block = img.crop(box)
                
                # 计算方块内所有像素的平均颜色
                pixels = block.getdata()  # 获取方块内所有像素的RGB值
                r_total, g_total, b_total = 0, 0, 0
                pixel_count = len(pixels)
                
                for pixel in pixels:
                    r_total += pixel[0]  # 累加红色值
                    g_total += pixel[1]  # 累加绿色值
                    b_total += pixel[2]  # 累加蓝色值
                
                # 计算平均RGB值
                avg_r = r_total // pixel_count
                avg_g = g_total // pixel_count
                avg_b = b_total // pixel_count
                
                # 用平均颜色填充整个方块
                for i in range(x, min(x + block_size, width)):
                    for j in range(y, min(y + block_size, height)):
                        mosaic_img.putpixel((i, j), (avg_r, avg_g, avg_b))

        # 保存处理后的图像
        mosaic_img.save(output_path)
        print(f"马赛克图像已保存到 {output_path}")
        
        # 显示图像（可选，适合本地运行）
        mosaic_img.show()

    except Exception as e:
        print(f"处理图像时出错：{e}")

# 程序入口
if __name__ == "__main__":
    # 定义输入和输出图像路径（需要替换为你自己的图像路径）
    input_image = "input.jpg"  # 替换为你的图像文件路径
    output_image = "mosaic_output.jpg"  # 输出文件名
    block_size = 15  # 马赛克方块大小，调整此值改变效果

    print("欢迎体验像素马赛克滤镜！")
    print(f"正在处理图像 {input_image}...")
    apply_mosaic_filter(input_image, output_image, block_size)
    print("处理完成！")