from PIL import Image  # 导入Pillow库的Image模块，用于图像处理
import os  # 导入os模块，用于处理文件和目录
import glob  # 导入glob模块，用于查找帧图像文件

def create_gif(input_folder, output_path, frame_duration=100, resize_width=200):
    """
    将文件夹中的帧图像拼接成循环GIF动画
    参数:
        input_folder: 包含帧图像的文件夹路径
        output_path: 输出GIF文件的路径
        frame_duration: 每帧显示时间（毫秒），控制动画速度
        resize_width: 调整帧图像的宽度（像素），保持宽高比
    """
    # 检查输入文件夹是否存在
    if not os.path.exists(input_folder):
        print(f"错误：找不到文件夹 {input_folder}！")
        return

    try:
        # 获取文件夹中所有图像文件（支持jpg和png格式）
        image_files = sorted(glob.glob(os.path.join(input_folder, "*.jpg")) + 
                            glob.glob(os.path.join(input_folder, "*.png")))
        
        # 检查是否有图像文件
        if not image_files:
            print(f"错误：文件夹 {input_folder} 中没有找到jpg或png图像！")
            return
        
        # 存储处理后的帧
        frames = []
        
        # 打开并处理每张图像
        for image_path in image_files:
            # 打开图像并转换为RGB模式（GIF需要RGB）
            img = Image.open(image_path).convert("RGB")
            
            # 调整图像大小，保持宽高比
            original_width, original_height = img.size
            aspect_ratio = original_height / original_width
            new_height = int(resize_width * aspect_ratio)
            img = img.resize((resize_width, new_height), Image.Resampling.LANCZOS)
            
            # 添加到帧列表
            frames.append(img)
        
        # 检查是否有有效帧
        if not frames:
            print("错误：没有成功加载任何帧图像！")
            return
        
        # 保存GIF动画
        # 第一帧作为基础，其他帧附加，设置循环播放
        frames[0].save(
            output_path,
            save_all=True,          # 保存所有帧
            append_images=frames[1:],  # 附加后续帧
            duration=frame_duration,   # 每帧显示时间（毫秒）
            loop=0                  # 0表示无限循环
        )
        
        print(f"GIF动画已保存到 {output_path}")
        
        # 显示GIF（可选，适合本地运行）
        try:
            os.startfile(output_path) if os.name == 'nt' else os.system(f"open {output_path}")
        except:
            print("无法自动打开GIF，请手动查看输出文件！")

    except Exception as e:
        print(f"创建GIF时出错：{e}")

# 程序入口
if __name__ == "__main__":
    # 定义输入文件夹和输出GIF路径（需要替换为实际路径）
    input_folder = "images/niao"  # 替换为包含帧图像的文件夹路径
    output_gif = "out/niao_animation.gif"  # 输出GIF文件名
    frame_duration = 100  # 每帧显示时间（毫秒），100ms约10帧/秒
    resize_width = 200    # 调整帧宽度，保持动画文件较小

    print("欢迎体验GIF动画师！")
    print(f"正在从文件夹 {input_folder} 创建GIF动画...")
    create_gif(input_folder, output_gif, frame_duration, resize_width)
    print("处理完成！")