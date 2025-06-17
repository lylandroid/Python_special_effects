import appcomm.utils.path_util as path_util

# --- 常量定义 ---
# 屏幕宽度和高度 (常量用大写字母表示)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# 窗口标题
WINDOW_TITLE = "星际保卫战"

FPS = 60

# --- 颜色定义 (RGB元组) ---
# 白色 (Red=255, Green=255, Blue=255)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0, 150)  # 绿色
# GREEN = (0, 255, 0)  # 绿色
RED = (255, 0, 0) # 红色
BLACK = (0, 0, 0) # 黑色
BACKGROUND_COLOR = (200, 200, 200) # 灰色
YELLOW = (255, 255, 0)
BROWN = (100, 50, 0)
SKY_BLUE = (135, 206, 235)
ORANGE = (255, 165, 0)


assets = path_util._Assets(__file__)