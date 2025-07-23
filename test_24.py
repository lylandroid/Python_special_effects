import cv2
import numpy as np
import random
from datetime import datetime
import os

class SketchEffect:
    def __init__(self):
        """初始化素描特效类"""
        # 创建窗口
        cv2.namedWindow("素描大师", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("素描大师", 800, 600)
        
        # 打开摄像头
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("无法打开摄像头")
            self.use_camera = False
        else:
            self.use_camera = True
        
        # 特效参数
        self.sketch_mode = 0  # 0: 铅笔素描, 1: 彩色素描, 2: 浮雕素描, 3: 卡通素描
        self.blur_size = 7    # 模糊核大小
        self.edge_strength = 255  # 边缘强度
        self.invert = False   # 是否反色
        self.show_original = False  # 是否显示原始画面
        
        # 图片文件相关
        self.image_path = None
        self.current_image = None
        
        # 创建控制面板
        self.create_control_panel()
        
        # 帧率计算
        self.prev_time = datetime.now()
        self.fps = 0
        
    def create_control_panel(self):
        """创建控制面板窗口"""
        cv2.namedWindow("控制面板", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("控制面板", 400, 400)
        
        # 创建滑动条
        cv2.createTrackbar("模糊大小", "控制面板", self.blur_size, 20, self.update_blur_size)
        cv2.createTrackbar("边缘强度", "控制面板", self.edge_strength, 255, self.update_edge_strength)
        cv2.createTrackbar("特效模式", "控制面板", self.sketch_mode, 3, self.update_sketch_mode)
        cv2.createTrackbar("显示原图", "控制面板", int(self.show_original), 1, self.update_show_original)
        cv2.createTrackbar("反色效果", "控制面板", int(self.invert), 1, self.update_invert)
        
        # 显示操作说明
        print("=== 素描大师特效程序 ===")
        print("操作说明:")
        print("1. 按 's' 键保存当前画面")
        print("2. 按 'q' 键退出程序")
        print("3. 按数字键 0-3 切换特效模式")
        print("4. 按 'i' 键加载图片文件")
        print("5. 按 'c' 键切换使用摄像头/图片")
        print("6. 调整控制面板中的滑动条来修改参数")
        
    def update_blur_size(self, value):
        """更新模糊核大小"""
        # 确保模糊核大小为奇数
        self.blur_size = max(1, value)
        if self.blur_size % 2 == 0:
            self.blur_size += 1
        cv2.setTrackbarPos("模糊大小", "控制面板", self.blur_size)
        
    def update_edge_strength(self, value):
        """更新边缘强度"""
        self.edge_strength = value
        
    def update_sketch_mode(self, value):
        """更新素描模式"""
        self.sketch_mode = value
        
    def update_show_original(self, value):
        """更新是否显示原始画面"""
        self.show_original = bool(value)
        
    def update_invert(self, value):
        """更新是否反色"""
        self.invert = bool(value)
        
    def calculate_fps(self):
        """计算帧率"""
        current_time = datetime.now()
        time_diff = (current_time - self.prev_time).total_seconds()
        self.fps = 1.0 / time_diff if time_diff > 0 else 0
        self.prev_time = current_time
        
    def load_image(self):
        """加载图片文件"""
        print("请输入图片路径 (例如: C:/images/test.jpg):")
        path = input().strip()
        
        if os.path.exists(path) and os.path.isfile(path):
            self.image_path = path
            self.current_image = cv2.imread(self.image_path)
            if self.current_image is not None:
                print(f"已加载图片: {self.image_path}")
                self.use_camera = False
                return True
            else:
                print("无法读取图片，请检查文件格式")
        else:
            print("文件不存在，请检查路径")
        return False
        
    def apply_sketch_effect(self, frame):
        """应用素描特效"""
        # 确保帧不为空
        if frame is None or frame.size == 0:
            return None
            
        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 应用高斯模糊减少噪点
        blurred = cv2.GaussianBlur(gray, (self.blur_size, self.blur_size), 0)
        
        # 根据素描模式处理图像
        if self.sketch_mode == 0:  # 铅笔素描
            # 计算灰度图像的反转
            if self.invert:
                inverted_blurred = 255 - blurred
            else:
                inverted_blurred = blurred
                
            # 创建铅笔素描效果
            sketch = cv2.divide(gray, inverted_blurred, scale=256.0)
            
            # 转换回BGR格式
            sketch_bgr = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
            
            # 调整边缘强度
            if self.edge_strength < 255:
                sketch_bgr = cv2.multiply(sketch_bgr, np.ones_like(sketch_bgr) * (self.edge_strength / 255.0), dtype=cv2.CV_8U)
                
            result = sketch_bgr
            
        elif self.sketch_mode == 1:  # 彩色素描
            # 应用双边滤波保留边缘同时平滑颜色
            color_sketch = cv2.bilateralFilter(frame, 9, 75, 75)
            
            # 创建边缘掩码
            edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY_INV, 11, 2)
            
            # 将边缘掩码转换为三通道
            edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            
            # 合并彩色和平滑效果
            result = cv2.bitwise_and(color_sketch, edges)
            
        elif self.sketch_mode == 2:  # 浮雕素描
            # 创建浮雕核
            kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
            
            # 应用浮雕效果
            embossed = cv2.filter2D(gray, -1, kernel)
            
            # 调整亮度
            embossed = cv2.add(embossed, 128)
            
            # 转换回BGR格式
            result = cv2.cvtColor(embossed, cv2.COLOR_GRAY2BGR)
            
        elif self.sketch_mode == 3:  # 卡通素描
            # 应用中值滤波减少噪点
            median_filtered = cv2.medianBlur(frame, 7)
            
            # 创建边缘掩码
            edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY_INV, 9, 2)
            
            # 应用颜色量化减少颜色数量，增强卡通效果
            num_colors = 7
            pixels = np.float32(median_filtered.reshape(-1, 3))
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
            _, labels, centers = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            centers = np.uint8(centers)
            cartoon = centers[labels.flatten()].reshape(median_filtered.shape)
            
            # 将边缘掩码转换为三通道
            edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            
            # 合并卡通和平滑效果
            result = cv2.bitwise_and(cartoon, edges)
        
        # 如果需要显示原始画面，则将素描效果叠加在原始画面上
        if self.show_original and frame is not None:
            # 调整透明度
            alpha = 0.5
            result = cv2.addWeighted(frame, alpha, result, 1 - alpha, 0)
            
        return result
        
    def run(self):
        """运行特效程序主循环"""
        frame_count = 0
        while True:
            # 获取当前帧
            if self.use_camera:
                ret, frame = self.cap.read()
                if not ret:
                    print("无法获取摄像头帧，退出程序")
                    break
            else:
                if self.current_image is not None:
                    # 复制当前加载的图片
                    frame = self.current_image.copy()
                else:
                    # 如果没有加载图片，显示空白帧
                    frame = np.zeros((480, 640, 3), dtype=np.uint8)
                    cv2.putText(frame, "请按 'i' 键加载图片", (100, 240), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # 计算帧率
            if frame_count % 10 == 0 and self.use_camera:  # 只在使用摄像头时计算帧率
                self.calculate_fps()
            frame_count += 1
                
            # 应用素描特效
            result = self.apply_sketch_effect(frame)
            
            # 在画面上显示信息
            if result is not None:
                # 显示帧率（仅当使用摄像头时）
                if self.use_camera:
                    cv2.putText(result, f"FPS: {self.fps:.1f}", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # 显示当前使用模式
                mode_text = ["铅笔素描", "彩色素描", "浮雕素描", "卡通素描"]
                source_text = "摄像头" if self.use_camera else "图片"
                cv2.putText(result, f"特效模式: {mode_text[self.sketch_mode]}", 
                           (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(result, f"来源: {source_text}", 
                           (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # 显示结果
                cv2.imshow("素描大师", result)
            
            # 处理键盘事件
            key = cv2.waitKey(1) & 0xFF
            
            # 按 'q' 键退出
            if key == ord('q'):
                break
                
            # 按 's' 键保存当前画面
            elif key == ord('s') and result is not None:
                filename = f"sketch_effect_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                cv2.imwrite(filename, result)
                print(f"已保存画面: {filename}")
                
            # 按数字键 0-3 切换特效模式
            elif key >= ord('0') and key <= ord('3'):
                self.sketch_mode = key - ord('0')
                cv2.setTrackbarPos("特效模式", "控制面板", self.sketch_mode)
                
            # 按 'i' 键加载图片
            elif key == ord('i'):
                self.load_image()
                
            # 按 'c' 键切换使用摄像头/图片
            elif key == ord('c'):
                if self.use_camera:
                    if self.current_image is not None:
                        self.use_camera = False
                        print("已切换到使用图片")
                    else:
                        print("请先加载图片")
                else:
                    if self.cap.isOpened():
                        self.use_camera = True
                        print("已切换到使用摄像头")
                    else:
                        print("摄像头不可用")
        
        # 释放资源
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()

# 主程序入口
if __name__ == "__main__":
    # 创建并运行素描特效程序
    effect = SketchEffect()
    effect.run()