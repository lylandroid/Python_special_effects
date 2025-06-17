import os
import time
import random
import threading
import sys
from colorama import init, Fore, Back, Style

# 初始化colorama以支持ANSI转义序列在Windows系统上正常工作
init(autoreset=True)

class Firework:
    """烟花类 - 负责单个烟花的发射、升空和爆炸效果"""
    
    def __init__(self, screen_width, screen_height):
        """初始化烟花属性"""
        self.width = screen_width  # 屏幕宽度
        self.height = screen_height  # 屏幕高度
        self.reset()  # 初始化烟花状态
        
    def reset(self):
        """重置烟花状态，准备下一次发射"""
        self.x = random.randint(5, self.width - 5)  # 随机发射位置
        self.y = self.height - 1  # 从屏幕底部发射
        self.speed = random.randint(2, 4)  # 升空速度
        self.exploded = False  # 是否已爆炸
        self.particles = []  # 爆炸后的粒子列表
        
        # 随机选择烟花颜色
        self.color = random.choice([
            Fore.RED, Fore.GREEN, Fore.YELLOW, 
            Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE
        ])
        
        # 随机选择烟花类型
        self.type = random.randint(1, 4)  # 四种烟花类型
    
    def launch(self):
        """发射烟花 - 更新烟花位置"""
        if not self.exploded:
            self.y -= self.speed  # 上升
            self.speed -= 0.1  # 减速
            
            # 到达顶点后爆炸
            if self.speed <= 0 or self.y <= self.height * 0.3:
                self.explode()
    
    def explode(self):
        """烟花爆炸 - 生成爆炸粒子"""
        self.exploded = True
        
        # 根据烟花类型生成不同的粒子效果
        if self.type == 1:  # 普通圆形烟花
            self._create_circle_particles()
        elif self.type == 2:  # 星形烟花
            self._create_star_particles()
        elif self.type == 3:  # 流星烟花
            self._create_meteor_particles()
        else:  # 随机混合烟花
            self._create_random_particles()
    
    def _create_circle_particles(self):
        """创建圆形烟花粒子"""
        particle_count = random.randint(30, 50)
        for i in range(particle_count):
            angle = 2 * 3.14159 * i / particle_count  # 均匀分布角度
            speed = random.uniform(0.5, 3)  # 随机速度
            self._add_particle(angle, speed, "circle")
    
    def _create_star_particles(self):
        """创建星形烟花粒子"""
        points = random.randint(5, 8)  # 星形的角数
        for i in range(points * 2):
            # 星形的内外半径不同
            radius = 2.5 if i % 2 == 0 else 1.0
            angle = 2 * 3.14159 * i / (points * 2)
            speed = radius * random.uniform(1.0, 2.0)
            self._add_particle(angle, speed, "star")
    
    def _create_meteor_particles(self):
        """创建流星烟花粒子"""
        particle_count = random.randint(10, 20)
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(2, 4)
            # 流星粒子更大，寿命更长
            self._add_particle(angle, speed, "meteor")
    
    def _create_random_particles(self):
        """创建随机混合烟花粒子"""
        particle_count = random.randint(20, 40)
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(0.5, 3)
            # 随机选择粒子类型
            particle_type = random.choice(["circle", "star", "trail"])
            self._add_particle(angle, speed, particle_type)
    
    def _add_particle(self, angle, speed, particle_type):
        """添加单个粒子到粒子列表"""
        # 计算粒子的速度分量
        vx = speed * 3.14159 * 0.1 * random.random() * (1 if random.random() > 0.5 else -1)
        vy = speed * 3.14159 * 0.1 * random.random() * (1 if random.random() > 0.5 else -1)
        
        # 根据粒子类型设置不同属性
        if particle_type == "circle":
            char = random.choice(['*', '•', '°'])
            life = random.randint(10, 30)
        elif particle_type == "star":
            char = random.choice(['✦', '✧', '★', '☆'])
            life = random.randint(15, 35)
        elif particle_type == "meteor":
            char = random.choice(['✦', '✧', '❉'])
            life = random.randint(20, 40)
        else:  # trail
            char = random.choice(['*', '+', 'o', '.'])
            life = random.randint(5, 20)
        
        # 为粒子添加随机颜色
        particle_color = random.choice([
            self.color, 
            random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, 
                         Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE])
        ])
        
        # 添加粒子到列表
        self.particles.append({
            'x': self.x,
            'y': self.y,
            'vx': vx,
            'vy': vy,
            'char': char,
            'color': particle_color,
            'life': life,
            'trail': []  # 粒子轨迹
        })
    
    def update_particles(self):
        """更新所有粒子的状态"""
        if not self.exploded:
            return
            
        # 更新每个粒子
        for particle in self.particles[:]:
            # 保存之前的位置用于轨迹
            if len(particle['trail']) < 3:  # 最多保存3个历史位置
                particle['trail'].append((int(particle['x']), int(particle['y'])))
            else:
                particle['trail'].pop(0)
                particle['trail'].append((int(particle['x']), int(particle['y'])))
            
            # 更新位置
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.05  # 重力效果
            particle['life'] -= 1  # 减少寿命
            
            # 移除寿命结束或超出屏幕的粒子
            if particle['life'] <= 0 or particle['y'] >= self.height or \
               particle['x'] < 0 or particle['x'] >= self.width:
                self.particles.remove(particle)
        
        # 如果所有粒子都消失了，重置烟花
        if not self.particles:
            self.reset()
    
    def draw(self, screen):
        """在屏幕上绘制烟花或其爆炸后的粒子"""
        if not self.exploded:
            # 绘制上升中的烟花
            if 0 <= self.y < self.height and 0 <= self.x < self.width:
                screen[int(self.y)][int(self.x)] = self.color + '^'
        else:
            # 绘制爆炸后的粒子及其轨迹
            for particle in self.particles:
                x, y = int(particle['x']), int(particle['y'])
                
                # 绘制粒子
                if 0 <= y < self.height and 0 <= x < self.width:
                    # 根据寿命计算亮度
                    alpha = min(1.0, particle['life'] / 10.0)
                    # 添加闪烁效果
                    if random.random() > 0.9:
                        char = random.choice(['*', '+', '.', '•'])
                    else:
                        char = particle['char']
                    
                    screen[y][x] = particle['color'] + char
                
                # 绘制粒子轨迹
                for i, (tx, ty) in enumerate(particle['trail']):
                    if 0 <= ty < self.height and 0 <= tx < self.width:
                        # 轨迹逐渐变淡
                        trail_alpha = 0.7 - i * 0.2
                        if trail_alpha > 0:
                            trail_char = '.'
                            screen[ty][tx] = particle['color'] + trail_char

class SoundEffect:
    """音效类 - 模拟烟花声效"""
    
    def __init__(self):
        """初始化音效库"""
        self.launch_sounds = [
            "嗖——", "咻——", "呼——", "呜——"
        ]
        self.explode_sounds = [
            "砰！！", "啪！！", "轰！！", "嘭！！", 
            "噼里啪啦！！", "轰啪！！"
        ]
    
    def play_launch(self):
        """播放发射音效"""
        return random.choice(self.launch_sounds)
    
    def play_explode(self):
        """播放爆炸音效"""
        return random.choice(self.explode_sounds)

class FireworksDisplay:
    """烟花展示类 - 管理整个烟花表演"""
    
    def __init__(self, width=80, height=20, fps=30):
        """初始化烟花展示属性"""
        self.width = width  # 屏幕宽度
        self.height = height  # 屏幕高度
        self.fps = fps  # 帧率
        self.frame_time = 1.0 / fps  # 每帧时间
        self.fireworks = [Firework(width, height) for _ in range(3)]  # 初始烟花
        self.running = False  # 是否运行中
        self.thread = None  # 运行线程
        self.sound = SoundEffect()  # 音效系统
        self.last_sound_time = 0  # 上次播放音效的时间
        self.sound_interval = 1.0  # 音效间隔时间
    
    def clear_screen(self):
        """清除屏幕"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def render(self):
        """渲染当前帧画面"""
        # 创建空白屏幕
        screen = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # 绘制所有烟花
        for firework in self.fireworks:
            firework.launch()
            firework.update_particles()
            firework.draw(screen)
        
        # 添加背景星星
        for _ in range(random.randint(10, 20)):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 3)  # 留出底部空间
            if screen[y][x] == ' ':
                # 闪烁的星星
                if random.random() > 0.8:
                    screen[y][x] = random.choice([
                        Fore.WHITE + '*', 
                        Fore.YELLOW + '.', 
                        Fore.CYAN + '•'
                    ])
        
        # 绘制地面
        ground_char = random.choice(['═', '─', '―', '━'])
        for x in range(self.width):
            screen[self.height - 1][x] = Fore.GREEN + ground_char
        
        # 添加互动提示
        hint = "按 Enter 键添加烟花 | 按 Q 键退出"
        screen[self.height - 2][:len(hint)] = list(Fore.WHITE + hint)
        
        # 将屏幕内容转为字符串
        output = '\n'.join([''.join(row) for row in screen])
        
        # 清除屏幕并显示当前帧
        self.clear_screen()
        print(output)
        
        # 随机播放音效
        current_time = time.time()
        if current_time - self.last_sound_time > self.sound_interval:
            if random.random() < 0.2:  # 20%概率播放音效
                if random.random() < 0.7:  # 70%是爆炸声
                    print(self.sound.play_explode())
                else:  # 30%是发射声
                    print(self.sound.play_launch())
                self.last_sound_time = current_time
    
    def run(self):
        """运行烟花展示"""
        self.running = True
        last_time = time.time()
        
        try:
            while self.running:
                current_time = time.time()
                elapsed = current_time - last_time
                
                # 控制帧率
                if elapsed >= self.frame_time:
                    self.render()
                    last_time = current_time
                    
                    # 随机添加新烟花
                    if random.random() < 0.05 and len(self.fireworks) < 8:
                        self.fireworks.append(Firework(self.width, self.height))
                
                # 短暂休眠
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            self.running = False
    
    def start(self):
        """在单独线程中启动烟花展示"""
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        """停止烟花展示"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
    
    def add_firework(self):
        """添加新烟花"""
        if len(self.fireworks) < 10:
            self.fireworks.append(Firework(self.width, self.height))
            return True
        return False

def get_user_input(fireworks):
    """获取用户输入并处理"""
    try:
        while fireworks.running:
            # 在Windows系统上使用msvcrt，在Linux/Mac上使用sys.stdin
            if os.name == 'nt':
                import msvcrt
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').lower()
                    if key == 'q':
                        fireworks.running = False
                    elif key == '\r':  # Enter键
                        if fireworks.add_firework():
                            print(fireworks.sound.play_launch())
            else:
                import sys, select
                if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                    key = sys.stdin.read(1).lower()
                    if key == 'q':
                        fireworks.running = False
                    elif key == '\n':  # Enter键
                        if fireworks.add_firework():
                            print(fireworks.sound.play_launch())
            time.sleep(0.1)
    except Exception as e:
        print(f"输入处理错误: {e}")

if __name__ == "__main__":
    # 获取终端大小或使用默认值
    try:
        rows, columns = os.get_terminal_size()
        width = min(columns - 1, 120)
        height = min(rows - 3, 30)
    except (OSError, ValueError):
        width, height = 80, 20
    
    # 创建并启动烟花展示
    fireworks = FireworksDisplay(width=width, height=height, fps=25)
    
    print("烟花表演开始！按 Enter 键添加烟花，按 Q 键退出...")
    
    # 启动烟花线程
    fireworks.start()
    
    # 启动用户输入线程
    input_thread = threading.Thread(target=get_user_input, args=(fireworks,))
    input_thread.daemon = True
    input_thread.start()
    
    # 等待主线程结束
    try:
        while fireworks.thread.is_alive():
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        pass
    finally:
        fireworks.stop()
        print("\n烟花表演已结束！")    