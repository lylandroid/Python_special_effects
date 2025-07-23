from PIL import Image, ImageFilter, ImageEnhance  # 导入Pillow库的模块，用于图像处理
import os  # 导入os模块，用于检查文件是否存在

def apply_watercolor_effect(input_path, output_path, blur_radius=5, color_boost=1.5):
    """
    为图像应用水彩画风格特效
    参数:
        input_path: 输入图像的路径
        output_path: 输出图像的路径
        blur_radius: 模糊半径，控制水彩的柔和程度
        color_boost: 颜色增强因子，增加水彩的鲜艳度
    """
    # 检查输入图像文件是否存在
    if not os.path.exists(input_path):
        print(f"错误：找不到图像文件 {input_path}！")
        return

    try:
        # 打开图像并转换为RGB模式
        img = Image.open(input_path).convert("RGB")
        
        # 步骤1：应用高斯模糊，模拟水彩的柔和边缘
        img_blurred = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        
        # 步骤2：增强颜色，增加水彩画的鲜艳感
        img_enhanced = ImageEnhance.Color(img_blurred).enhance(color_boost)
        
        # 步骤3：检测边缘，模拟水彩画的轮廓线
        img_edges = img.filter(ImageFilter.FIND_EDGES)
        # 将边缘图像转换为灰度并增强对比度
        img_edges = img_edges.convert("L").filter(ImageFilter.EDGE_ENHANCE)
        
        # 步骤4：将边缘叠加回模糊图像，创造水彩效果
        # 将边缘图像转换回RGB以便与原图混合
        img_edges_rgb = img_edges.convert("RGB")
        # 创建新图像，混合模糊图像和边缘
        img_final = Image.blend(img_enhanced, img_edges_rgb, alpha=0.2)
        
        # 步骤5：增加整体亮度和对比度，增强水彩质感
        img_final = ImageEnhance.Brightness(img_final).enhance(1.1)
        img_final = ImageEnhance.Contrast(img_final).enhance(1.2)
        
        # 保存处理后的图像
        img_final.save(output_path)
        print(f"水彩画图像已保存到 {output_path}")
        
        # 显示图像（可选，适合本地运行）
        img_final.show()

    except Exception as e:
        print(f"处理图像时出错：{e}")

# 程序入口
if __name__ == "__main__":
    # 定义输入和输出图像路径（需要替换为实际图像路径）
    input_image = "images/meizhao2.jpg"  # 替换为你的图像文件路径
    output_image = "images_target/watercolor_output.jpg"  # 输出文件名
    blur_radius = 5  # 模糊半径，调整以改变柔和度
    color_boost = 1.5  # 颜色增强因子，调整以改变鲜艳度

    print("欢迎体验水彩奇观特效！")
    print(f"正在处理图像 {input_image}...")
    apply_watercolor_effect(input_image, output_image, blur_radius, color_boost)
    print("处理完成！")