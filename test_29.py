import cv2

# 读取图像
image = cv2.imread("images/katong.png")  # 替换为你的图片路径
if image is None:
    print("图像读取失败，请检查路径")
    exit()

# 调整图像大小（可选）
image = cv2.resize(image, (600, 400))

# 第一步：应用双边滤波，模糊颜色但保留边缘
# d是像素邻域的直径，sigmaColor和sigmaSpace是滤波强度
color_image = cv2.bilateralFilter(image, d=9, sigmaColor=300, sigmaSpace=300)

# 第二步：提取边缘线条
# 将图像转为灰度
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 使用中值滤波去噪
blurred = cv2.medianBlur(gray, 7)

# 使用自适应阈值得到轮廓
edges = cv2.adaptiveThreshold(
    blurred,
    255,
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY,
    blockSize=9,
    C=2
)

# 第三步：将边缘图转换为彩色（和原图一样的3通道）
edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

# 第四步：将边缘线叠加到双边滤波图像上，形成卡通效果
cartoon = cv2.bitwise_and(color_image, edges_colored)

# 显示图像
cv2.imshow("原图", image)
cv2.imshow("卡通人物效果", cartoon)

# 保存结果（可选）
cv2.imwrite("out/cartoon_output.jpg", cartoon)

# 等待按键退出
cv2.waitKey(0)
cv2.destroyAllWindows()
