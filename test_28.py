import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance
import numpy as np

class SepiaFilterApp:
    def __init__(self, root):
        """初始化棕褐色滤镜应用"""
        self.root = root
        self.root.title("复古风情 - 棕褐色滤镜")
        self.root.geometry("900x650")
        self.root.configure(bg="#f0f0f0")
        
        # 确保中文正常显示
        self.font_config = ("SimHei", 12)
        
        # 初始化变量
        self.original_img = None
        self.modified_img = None
        self.tk_original = None
        self.tk_modified = None
        
        # 效果参数
        self.sepia_intensity = 0.8  # 棕褐色强度
        self.contrast_factor = 1.2  # 对比度因子
        self.brightness_factor = 1.0  # 亮度因子
        
        self.create_widgets()
        
    def create_widgets(self):
        """创建GUI组件"""
        # 顶部标题
        title_label = tk.Label(self.root, text="复古风情 - 棕褐色滤镜", 
                             font=("SimHei", 18, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)
        
        # 控制区域
        control_frame = tk.Frame(self.root, bg="#f0f0f0")
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 加载图片按钮
        load_btn = tk.Button(control_frame, text="加载图片", font=self.font_config, 
                            command=self.load_image, bg="#4CAF50", fg="white",
                            relief=tk.RAISED, padx=10)
        load_btn.pack(side=tk.LEFT, padx=10)
        
        # 应用棕褐色滤镜按钮
        apply_btn = tk.Button(control_frame, text="应用棕褐色滤镜", font=self.font_config,
                             command=self.apply_sepia_filter, bg="#2196F3", fg="white",
                             relief=tk.RAISED, padx=10)
        apply_btn.pack(side=tk.LEFT, padx=10)
        
        # 保存图片按钮
        save_btn = tk.Button(control_frame, text="保存图片", font=self.font_config,
                            command=self.save_image, bg="#f44336", fg="white",
                            relief=tk.RAISED, padx=10)
        save_btn.pack(side=tk.RIGHT, padx=10)
        
        # 效果参数调节区域
        params_frame = tk.LabelFrame(self.root, text="效果参数", font=self.font_config, bg="#f0f0f0")
        params_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # 棕褐色强度滑块
        sepia_frame = tk.Frame(params_frame, bg="#f0f0f0")
        sepia_frame.pack(fill=tk.X, padx=10, pady=5)
        
        sepia_label = tk.Label(sepia_frame, text="棕褐色强度:", font=self.font_config, bg="#f0f0f0")
        sepia_label.pack(side=tk.LEFT, padx=5)
        
        self.sepia_scale = tk.Scale(sepia_frame, from_=0, to=10, orient=tk.HORIZONTAL,
                                  length=200, resolution=0.1, command=self.update_sepia_intensity,
                                  bg="#f0f0f0", highlightthickness=0)
        self.sepia_scale.set(self.sepia_intensity * 10)
        self.sepia_scale.pack(side=tk.LEFT, padx=5)
        
        # 对比度滑块
        contrast_frame = tk.Frame(params_frame, bg="#f0f0f0")
        contrast_frame.pack(fill=tk.X, padx=10, pady=5)
        
        contrast_label = tk.Label(contrast_frame, text="对比度:", font=self.font_config, bg="#f0f0f0")
        contrast_label.pack(side=tk.LEFT, padx=5)
        
        self.contrast_scale = tk.Scale(contrast_frame, from_=0.5, to=2.0, orient=tk.HORIZONTAL,
                                     length=200, resolution=0.1, command=self.update_contrast,
                                     bg="#f0f0f0", highlightthickness=0)
        self.contrast_scale.set(self.contrast_factor)
        self.contrast_scale.pack(side=tk.LEFT, padx=5)
        
        # 亮度滑块
        brightness_frame = tk.Frame(params_frame, bg="#f0f0f0")
        brightness_frame.pack(fill=tk.X, padx=10, pady=5)
        
        brightness_label = tk.Label(brightness_frame, text="亮度:", font=self.font_config, bg="#f0f0f0")
        brightness_label.pack(side=tk.LEFT, padx=5)
        
        self.brightness_scale = tk.Scale(brightness_frame, from_=0.5, to=2.0, orient=tk.HORIZONTAL,
                                        length=200, resolution=0.1, command=self.update_brightness,
                                        bg="#f0f0f0", highlightthickness=0)
        self.brightness_scale.set(self.brightness_factor)
        self.brightness_scale.pack(side=tk.LEFT, padx=5)
        
        # 图片显示区域
        image_frame = tk.Frame(self.root, bg="#e0e0e0", bd=2, relief=tk.SUNKEN)
        image_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 原始图片区域
        original_frame = tk.LabelFrame(image_frame, text="原始图片", font=self.font_config, bg="#e0e0e0")
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.original_label = tk.Label(original_frame, bg="#cccccc")
        self.original_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 修改后图片区域
        modified_frame = tk.LabelFrame(image_frame, text="棕褐色效果", font=self.font_config, bg="#e0e0e0")
        modified_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.modified_label = tk.Label(modified_frame, bg="#cccccc")
        self.modified_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 底部信息
        info_label = tk.Label(self.root, text="提示: 调整参数并点击应用棕褐色滤镜按钮来生成不同的复古效果", 
                             font=("SimHei", 10), bg="#f0f0f0", fg="#666666")
        info_label.pack(pady=5)
        
    def load_image(self):
        """加载图片文件"""
        file_path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("图片文件", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
        )
        
        if file_path:
            try:
                self.original_img = Image.open(file_path).convert("RGB")
                # 调整图片大小以适应显示区域
                self.original_img.thumbnail((400, 400))
                self.tk_original = ImageTk.PhotoImage(self.original_img)
                self.original_label.config(image=self.tk_original)
                
                # 重置修改后的图片
                self.modified_img = None
                self.modified_label.config(image=None)
                
                messagebox.showinfo("成功", "图片加载成功！")
            except Exception as e:
                messagebox.showerror("错误", f"加载图片失败: {str(e)}")
    
    def update_sepia_intensity(self, value):
        """更新棕褐色强度"""
        self.sepia_intensity = float(value) / 10.0
    
    def update_contrast(self, value):
        """更新对比度"""
        self.contrast_factor = float(value)
    
    def update_brightness(self, value):
        """更新亮度"""
        self.brightness_factor = float(value)
    
    def apply_sepia_filter(self):
        """应用棕褐色滤镜"""
        if self.original_img:
            try:
                # 应用棕褐色滤镜
                self.modified_img = self.create_sepia_effect(
                    self.original_img, 
                    self.sepia_intensity,
                    self.contrast_factor,
                    self.brightness_factor
                )
                
                self.tk_modified = ImageTk.PhotoImage(self.modified_img)
                self.modified_label.config(image=self.tk_modified)
                
                messagebox.showinfo("成功", "棕褐色滤镜应用成功！")
            except Exception as e:
                messagebox.showerror("错误", f"应用棕褐色滤镜失败: {str(e)}")
    
    def create_sepia_effect(self, img, intensity, contrast, brightness):
        """创建棕褐色效果"""
        # 复制原始图像
        sepia_img = img.copy()
        
        # 调整对比度
        if contrast != 1.0:
            enhancer = ImageEnhance.Contrast(sepia_img)
            sepia_img = enhancer.enhance(contrast)
        
        # 调整亮度
        if brightness != 1.0:
            enhancer = ImageEnhance.Brightness(sepia_img)
            sepia_img = enhancer.enhance(brightness)
        
        # 转换为RGB数组以便处理
        pixels = np.array(sepia_img)
        
        # 应用棕褐色滤镜
        # 棕褐色滤镜的转换公式
        # R' = 0.393R + 0.769G + 0.189B
        # G' = 0.349R + 0.686G + 0.168B
        # B' = 0.272R + 0.534G + 0.131B
        r, g, b = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]
        
        # 计算新的RGB值
        new_r = np.clip(0.393 * r + 0.769 * g + 0.189 * b, 0, 255).astype(np.uint8)
        new_g = np.clip(0.349 * r + 0.686 * g + 0.168 * b, 0, 255).astype(np.uint8)
        new_b = np.clip(0.272 * r + 0.534 * g + 0.131 * b, 0, 255).astype(np.uint8)
        
        # 创建棕褐色图像
        sepia_pixels = np.dstack((new_r, new_g, new_b))
        sepia_result = Image.fromarray(sepia_pixels)
        
        # 根据强度混合原始图像和棕褐色图像
        if intensity < 1.0:
            sepia_img = Image.blend(img, sepia_result, intensity)
        else:
            sepia_img = sepia_result
        
        return sepia_img
    
    def save_image(self):
        """保存修改后的图片"""
        if self.modified_img:
            try:
                file_path = filedialog.asksaveasfilename(
                    title="保存图片",
                    defaultextension=".png",
                    filetypes=[("PNG 文件", "*.png"), ("JPEG 文件", "*.jpg")]
                )
                
                if file_path:
                    self.modified_img.save(file_path)
                    messagebox.showinfo("成功", f"图片已保存至: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存图片失败: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SepiaFilterApp(root)
    root.mainloop()    