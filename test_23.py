import cv2
import numpy as np
import random
from datetime import datetime

class EdgeDetectionEffect:
    def __init__(self):
        """初始化边缘检测特效类"""
        # 创建窗口
        cv2.namedWindow("边缘检测特效", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("边缘检测特效", 800, 600)
        
        # 打开摄像头
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("无法打开摄像头，尝试使用示例视频")
            # 如果无法打开摄像头，使用示例视频文件
            self.cap = cv2.VideoCapture("example_video.mp4")
            if not self.cap.isOpened():
                raise ValueError("无法打开摄像头或示例视频文件")
        
        # 特效参数
        self.effect_mode = 0  # 0: 普通边缘, 1: 彩色边缘, 2: 霓虹边缘, 3: 随机边缘
        self.threshold1 = 100  # Canny边缘检测低阈值
        self.threshold2 = 200  # Canny边缘检测高阈值
        self.show_original = False  # 是否显示原始画面
        self.edge_color = (255, 255, 255)  # 默认边缘颜色(白色)
        
        # 创建控制面板
        self.create_control_panel()
        
        # 帧率计算
        self.prev_time = datetime.now()
        self.fps = 0
        
    def create_control_panel(self):
        """创建控制面板窗口"""
        cv2.namedWindow("控制面板", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("控制面板", 400, 300)
        
        # 创建滑动条
        cv2.createTrackbar("低阈值", "控制面板", self.threshold1, 300, self.update_threshold1)
        cv2.createTrackbar("高阈值", "控制面板", self.threshold2, 300, self.update_threshold2)
        cv2.createTrackbar("特效模式", "控制面板", self.effect_mode, 3, self.update_effect_mode)
        cv2.createTrackbar("显示原图", "控制面板", int(self.show_original), 1, self.update_show_original)
        
        # 显示操作说明
        print("=== 边缘检测特效程序 ===")
        print("操作说明:")
        print("1. 按 's' 键保存当前画面")
        print("2. 按 'q' 键退出程序")
        print("3. 按数字键 0-3 切换特效模式")
        print("4. 调整控制面板中的滑动条来修改参数")
        
    def update_threshold1(self, value):
        """更新Canny边缘检测的低阈值"""
        self.threshold1 = max(1, value)  # 确保阈值至少为1
        
    def update_threshold2(self, value):
        """更新Canny边缘检测的高阈值"""
        self.threshold2 = max(1, value)  # 确保阈值至少为1
        
    def update_effect_mode(self, value):
        """更新特效模式"""
        self.effect_mode = value
        
    def update_show_original(self, value):
        """更新是否显示原始画面"""
        self.show_original = bool(value)
        
    def calculate_fps(self):
        """计算帧率"""
        current_time = datetime.now()
        time_diff = (current_time - self.prev_time).total_seconds()
        self.fps = 1.0 / time_diff if time_diff > 0 else 0
        self.prev_time = current_time
        
    def apply_edge_effect(self, frame):
        """应用边缘检测特效"""
        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 使用Canny算法进行边缘检测
        edges = cv2.Canny(gray, self.threshold1, self.threshold2)
        
        # 根据特效模式处理边缘
        if self.effect_mode == 0:  # 普通边缘
            # 创建一个黑色背景，然后将白色边缘绘制在上面
            edge_frame = np.zeros_like(frame)
            edge_frame[edges > 0] = self.edge_color
            
        elif self.effect_mode == 1:  # 彩色边缘
            # 将边缘检测结果扩展为三通道
            edges_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            # 使用原始图像的颜色作为边缘颜色
            edge_frame = cv2.bitwise_and(frame, edges_color)
            
        elif self.effect_mode == 2:  # 霓虹边缘
            # 创建一个黑色背景
            edge_frame = np.zeros_like(frame)
            # 生成随机霓虹颜色
            neon_color = (random.randint(150, 255), 
                          random.randint(150, 255), 
                          random.randint(150, 255))
            # 将边缘绘制为霓虹颜色
            edge_frame[edges > 0] = neon_color
            
            # 添加模糊效果增强霓虹感
            edge_frame = cv2.GaussianBlur(edge_frame, (5, 5), 0)
            
        elif self.effect_mode == 3:  # 随机边缘
            # 创建一个黑色背景
            edge_frame = np.zeros_like(frame)
            # 为每个边缘像素随机分配颜色
            for i in range(edges.shape[0]):
                for j in range(edges.shape[1]):
                    if edges[i, j] > 0:
                        edge_frame[i, j] = (random.randint(0, 255), 
                                           random.randint(0, 255), 
                                           random.randint(0, 255))
        
        # 如果需要显示原始画面，则将边缘叠加在原始画面上
        if self.show_original:
            result = cv2.addWeighted(frame, 0.7, edge_frame, 1.0, 0)
        else:
            result = edge_frame
            
        return result
        
    def run(self):
        """运行特效程序主循环"""
        frame_count = 0
        while True:
            # 读取一帧
            ret, frame = self.cap.read()
            if not ret:
                print("无法获取帧，退出程序")
                break
                
            # 计算帧率
            if frame_count % 10 == 0:  # 每10帧计算一次，减少计算负担
                self.calculate_fps()
            frame_count += 1
                
            # 应用边缘检测特效
            result = self.apply_edge_effect(frame)
            
            # 在画面上显示帧率
            cv2.putText(result, f"FPS: {self.fps:.1f}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                       
            # 在画面上显示当前特效模式
            mode_text = ["普通边缘", "彩色边缘", "霓虹边缘", "随机边缘"]
            cv2.putText(result, f"特效模式: {mode_text[self.effect_mode]}", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                       
            # 显示结果
            cv2.imshow("边缘检测特效", result)
            
            # 处理键盘事件
            key = cv2.waitKey(1) & 0xFF
            
            # 按 'q' 键退出
            if key == ord('q'):
                break
                
            # 按 's' 键保存当前画面
            elif key == ord('s'):
                filename = f"edge_effect_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                cv2.imwrite(filename, result)
                print(f"已保存画面: {filename}")
                
            # 按数字键 0-3 切换特效模式
            elif key >= ord('0') and key <= ord('3'):
                self.effect_mode = key - ord('0')
                cv2.setTrackbarPos("特效模式", "控制面板", self.effect_mode)
                
        # 释放资源
        self.cap.release()
        cv2.destroyAllWindows()

# 主程序入口
if __name__ == "__main__":
    # 创建并运行边缘检测特效程序
    effect = EdgeDetectionEffect()
    effect.run()