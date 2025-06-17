import pygame
import os

class ImageLoader:
    """
    图像加载工具类，用于简化 Pygame 中的图像加载和处理
    提供安全、易用的图像管理功能
    """
    
    def __init__(self):
        """初始化工具类，设置默认参数"""
        if not pygame.get_init():
            pygame.init()  # 确保 Pygame 已初始化
        # self.images = {}  # 存储已加载的图像，键为文件名，值为图像对象
        
        self.default_scale = (100, 100)  # 默认缩放尺寸
        self.scale_80 = (80, 80) 
        self.scale_50 = (50, 50) 

        self.default_alpha = 255  # 默认透明度（0-255，255为不透明）

    def load_image(self, file_path):
        """
        加载图像并存储
        参数:
            file_path: 图像文件路径（支持 PNG、JPG 等）
        返回:
            加载的图像对象（pygame.Surface）
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                print(f"错误: 图像文件 {file_path} 不存在")
                return None
            
            # 加载图像
            image = pygame.image.load(file_path)
            # 转换为 Pygame 内部格式以优化性能
            image = image.convert_alpha()
            # 存储到字典
            # self.images[file_path] = image
            # print(f"成功加载图像: {file_path}")
            return image
            
        except pygame.error as e:
            print(f"加载图像失败: {e}")
            return None
        except Exception as e:
            print(f"未知错误: {e}")
            return None

    def get_image(self, file_path):
        """
        获取已加载的图像，未加载则尝试加载
        参数:
            file_path: 图像文件路径
        返回:
            图像对象或 None
        """
        # if file_path in self.images:
        #     return self.images[file_path]
        return self.load_image(file_path)

    def scale_image(self, image, size=None):
        """
        缩放图像
        参数:
            image: 图像对象（pygame.Surface）
            size: 目标尺寸 (宽, 高)，默认使用 self.default_scale
        返回:
            缩放后的图像对象
        """
        if image is None:
            print("错误: 无法缩放空图像")
            return None
        
        try:
            size = size or self.default_scale
            scaled_image = pygame.transform.scale(image, size)
            return scaled_image
        except Exception as e:
            print(f"缩放图像失败: {e}")
            return image

    def rotate_image(self, image, angle):
        """
        旋转图像
        参数:
            image: 图像对象
            angle: 旋转角度（度，顺时针）
        返回:
            旋转后的图像对象
        """
        if image is None:
            print("错误: 无法旋转空图像")
            return None
        
        try:
            rotated_image = pygame.transform.rotate(image, angle)
            return rotated_image
        except Exception as e:
            print(f"旋转图像失败: {e}")
            return image

    def set_alpha(self, image, alpha=None):
        """
        设置图像透明度
        参数:
            image: 图像对象
            alpha: 透明度值（0-255，0为完全透明），默认使用 self.default_alpha
        返回:
            设置透明度后的图像对象
        """
        if image is None:
            print("错误: 无法设置空图像透明度")
            return None
        
        try:
            alpha = alpha or self.default_alpha
            image.set_alpha(alpha)
            return image
        except Exception as e:
            print(f"设置透明度失败: {e}")
            return image

    def clear_images(self):
        """清空已加载的图像，释放内存"""
        # self.images.clear()
        print("已清空所有图像")



img_loader = ImageLoader()

