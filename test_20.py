# ----------------------------------------------------
# Python 少儿编程 - 创意特效：随机迷宫生成器
#
# 这个项目会教我们：
# 1. 如何用“类”和“网格”来表示一个复杂结构（迷宫）。
# 2. 一个经典的迷宫生成算法：“深度优先搜索”与“回溯法”。
# 3. 什么是“栈”数据结构，以及如何用它来追踪我们的路径。
# 4. 如何将算法的执行过程进行可视化，创造出酷炫的动画效果。
# ----------------------------------------------------

import pygame
import random

# --- 1. 初始化 Pygame 和设置 ---
pygame.init()

# 屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("随机迷宫生成器 by Gemini")

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0) # 用来高亮显示当前正在“挖掘”的单元格

# 迷宫网格设置
CELL_SIZE = 20 # 每个单元格的大小（像素）
COLS = SCREEN_WIDTH // CELL_SIZE
ROWS = SCREEN_HEIGHT // CELL_SIZE

# 创建时钟对象
clock = pygame.time.Clock()

# --- 2. 单元格类 (Cell Class) ---
# 这是迷宫的基本组成部分，每个小方格都是一个 Cell 对象
class Cell:
    def __init__(self, x, y):
        self.x = x # 单元格的列号 (column)
        self.y = y # 单元格的行号 (row)
        
        # 每面墙都存在，直到我们把它“推倒”
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False # 记录这个单元格是否被访问过

    # 绘制单元格的墙
    def draw(self):
        # 计算单元格在屏幕上的真实坐标
        px = self.x * CELL_SIZE
        py = self.y * CELL_SIZE
        
        if self.walls['top']:
            pygame.draw.line(screen, WHITE, (px, py), (px + CELL_SIZE, py), 1)
        if self.walls['right']:
            pygame.draw.line(screen, WHITE, (px + CELL_SIZE, py), (px + CELL_SIZE, py + CELL_SIZE), 1)
        if self.walls['bottom']:
            pygame.draw.line(screen, WHITE, (px + CELL_SIZE, py + CELL_SIZE), (px, py + CELL_SIZE), 1)
        if self.walls['left']:
            pygame.draw.line(screen, WHITE, (px, py + CELL_SIZE), (px, py), 1)

    # 检查并返回周围未被访问过的邻居
    def check_neighbors(self, grid):
        neighbors = []
        # 定义邻居的相对位置 (行, 列)
        # 上: (y-1, x), 右: (y, x+1), 下: (y+1, x), 左: (y, x-1)
        top = grid[self.y - 1][self.x] if self.y > 0 else None
        right = grid[self.y][self.x + 1] if self.x < COLS - 1 else None
        bottom = grid[self.y + 1][self.x] if self.y < ROWS - 1 else None
        left = grid[self.y][self.x - 1] if self.x > 0 else None

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)

        if len(neighbors) > 0:
            return random.choice(neighbors) # 随机返回一个邻居
        else:
            return None

# --- 3. 辅助函数 ---
# 推倒两个单元格之间的墙
def remove_walls(current_cell, next_cell):
    dx = current_cell.x - next_cell.x
    dy = current_cell.y - next_cell.y
    
    if dx == 1: # current 在 next 的右边
        current_cell.walls['left'] = False
        next_cell.walls['right'] = False
    elif dx == -1: # current 在 next 的左边
        current_cell.walls['right'] = False
        next_cell.walls['left'] = True
    
    if dy == 1: # current 在 next 的下边
        current_cell.walls['top'] = False
        next_cell.walls['bottom'] = False
    elif dy == -1: # current 在 next 的上边
        current_cell.walls['bottom'] = False
        next_cell.walls['top'] = True

# --- 4. 主程序和生成逻辑 ---
# 创建网格，填满 Cell 对象
grid = [[Cell(x, y) for x in range(COLS)] for y in range(ROWS)]

# 算法的起始点
current_cell = grid[0][0]
current_cell.visited = True

# “栈”是一个重要的数据结构，用来存储我们走过的路径，方便“回溯”
# 我们可以把它想象成一串脚印，迷路了可以沿着脚印原路返回
the_stack = [current_cell]

# 迷宫生成完成的标志
maze_generated = False

running = True
while running:
    # --- a. 事件处理 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- b. 绘制 ---
    screen.fill(BLACK) # 用黑色清空屏幕
    # 绘制所有单元格
    for row in grid:
        for cell in row:
            cell.draw()

    # --- c. 迷宫生成算法 (每帧执行一步，实现动画效果) ---
    if not maze_generated:
        if len(the_stack) > 0:
            current_cell = the_stack[-1] # 查看栈顶的元素，也就是我们当前的位置
            
            # 高亮显示当前单元格
            px = current_cell.x * CELL_SIZE
            py = current_cell.y * CELL_SIZE
            pygame.draw.rect(screen, GREEN, (px, py, CELL_SIZE, CELL_SIZE))
            
            # 1. 寻找一个未被访问过的邻居
            next_cell = current_cell.check_neighbors(grid)
            
            if next_cell:
                next_cell.visited = True
                
                # 2. 把这个邻居压入栈中，记录路径
                the_stack.append(next_cell)
                
                # 3. 推倒两个单元格之间的墙
                remove_walls(current_cell, next_cell)
                
            else:
                # 4. 如果没有可走的邻居（死路一条），就从栈中弹出一个元素
                # 这就是“回溯”，就像沿着脚印原路返回，去寻找别的出路
                the_stack.pop()
        else:
            # 如果栈空了，说明所有单元格都访问过了，迷宫生成完毕！
            maze_generated = True
            print("迷宫生成完毕！")


    # --- d. 刷新屏幕 ---
    pygame.display.flip()

    # --- e. 控制帧率 ---
    # 我们可以通过调整帧率来控制迷宫生成的速度
    clock.tick(60)

# --- 5. 退出程序 ---
pygame.quit()