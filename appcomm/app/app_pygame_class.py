import pygame
import sys
import appcomm.config_class as config
from appcomm.abstract.abs_main_pygame_class import *

class _BasePygame:
    _main_listener : AbsMainPygameListener = None
    running = True

    def __init__(self):
         # --- 初始化Pygame和窗口 ---
        if not pygame.get_init():
            pygame.init()
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.WINDOW_TITLE)
        
        self.clock = pygame.time.Clock()
    
    # 主逻辑
    def run(self):
        while(self.running):
            # 处理事件
            self.  _handle_events()

            # 处理循环体逻辑
            if self._main_listener.app_handle_update() is False:
                self.running = False

            # 处理绘制逻辑
            self._main_listener.app_draw(self.screen)
                
            self.clock.tick(config.FPS)

    # 处理 event 事件
    def _handle_events(self):
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self._main_listener.app_handle_event(event) is False:
                self.running = False
                
        
    def app_quit(self):
        if self._main_listener is not None:
             # 释放资源
            self._main_listener.app_handle_quit()
            self._main_listener = None

        pygame.quit()
        sys.exit()


class AppPygame(_BasePygame):

    def __init__(self, main_listener : AbsMainPygameListener):
        super().__init__()

        # 统一调用流程
        self._main_listener = main_listener

        self.run()
        self.app_quit()
      




    
