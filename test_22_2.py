# 导入必要的库
import cv2  # OpenCV 库，用于图像处理
from PIL import Image, ImageFilter  # PIL 库，也称为 Pillow，用于图像处理
import numpy as np  # 导入 NumPy 库，用于数组操作，OpenCV 图像本质上是 NumPy 数组

def 梦幻模糊(image_path, output_path, blur_radius=10):
    """
    对图像应用梦幻模糊效果。

    参数:
    image_path (str): 输入图像的路径。
    output_path (str): 输出图像的路径。
    blur_radius (int): 高斯模糊的半径，数值越大，模糊效果越强。
    """

    # 1. 使用 OpenCV 读取图像
    img_cv = cv2.imread(image_path)

    # 检查图像是否成功读取
    if img_cv is None:
        print(f"错误：无法读取图像文件 {image_path}。请检查路径和文件是否存在。")
        return

    # 2. 将 OpenCV 的图像格式转换为 PIL 的图像格式 (BGR -> RGB)
    img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))

    # 3. 应用高斯模糊
    blurred_img = img_pil.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # 4. 创建一个覆盖层，用于增加亮度 (可选，用于增强梦幻感)
    # PIL Image.new 接受模式、大小和颜色
    # RGBA 模式允许透明度，(255, 255, 255, 50) 表示白色，透明度为 50 (0-255)
    overlay = Image.new('RGBA', blurred_img.size, (255, 255, 255, 50))

    # 5. 将覆盖层与模糊后的图像合并
    # Image.blend(image1, image2, alpha) 根据 alpha 值混合两张图像
    # alpha 值为 0.2 意味着 80% 的 blurred_img 和 20% 的 overlay
    combined_img = Image.blend(blurred_img.convert('RGBA'), overlay, 0.2)

    # 6. 将图像从 PIL 格式转换回 OpenCV 格式
    # PIL 图像需要先转换为 NumPy 数组，然后从 RGBA 转换为 BGR
    img_cv_output = cv2.cvtColor(np.array(combined_img), cv2.COLOR_RGBA2BGR)

    # 7. 保存图像
    cv2.imwrite(output_path, img_cv_output)

    print(f"梦幻模糊效果已应用并保存到: {output_path}")

# 示例用法
if __name__ == "__main__":
    # 请将 'input.jpg' 替换为你自己的图像文件路径
    # 确保你的 Python 脚本所在的目录下有这张图片，或者提供完整的路径
    input_image = "images/gou2-2.jpg"
    output_image = "output_dreamy_blur.jpg"
    blur_radius = 15  # 你可以调整这个值来改变模糊的程度 (通常是奇数，但PIL接受偶数)

    梦幻模糊(input_image, output_image, blur_radius)