# 导入Pillow库，用于图像处理
from PIL import Image, ImageOps

def create_color_invert(input_path, output_path, enhance_factor=1.0):
    """
    将输入图像的颜色反转，生成超现实效果并保存
    参数:
        input_path: 输入图像的路径
        output_path: 输出反转效果的路径
        enhance_factor: 对比度增强因子，控制效果鲜艳度（建议0.5-2.0）
    """
    # 打开输入图像
    image = Image.open(input_path)
    
    # 确保图像是RGB模式（颜色反转需要RGB通道）
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # 反转图像颜色，生成负片效果
    inverted_image = ImageOps.invert(image)
    
    # 可选：增强对比度，使颜色反转效果更鲜艳
    if enhance_factor != 1.0:
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(inverted_image)
        inverted_image = enhancer.enhance(enhance_factor)
    
    # 保存反转后的图像
    inverted_image.save(output_path)
    print(f"颜色反转图像已保存到: {output_path}")

# 示例用法
if __name__ == "__main__":
    # 输入和输出路径（需要替换为实际图片路径）
    input_image = "images/gou3.png"  # 替换为你的照片路径
    output_image = "color_inverted_output.jpg"
    
    # 调用函数生成颜色反转效果
    create_color_invert(input_image, output_image, enhance_factor=1.2)