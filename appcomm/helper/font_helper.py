# 字体模块
import pygame
import appcomm.utils.path_util as path_util
from typing import Any

# 字体工具类
class FontHelper:
    # 字体初始化，没有字体文件传 file_uri = None
    def __init__(self, _file, file_uri : str, font_size = 36):
        if not pygame.font.get_init():
            pygame.font.init()
       
        if _file is not None:
            self.path = path_util.join_file_uri(_file, file_uri)
        elif file_uri is not None:
            self.path = file_uri
        else:
            self.path = path_util.join(path_util.get_parent_dir(__file__), "assets/fonts/fonts.ttf")
            
        self.font = pygame.font.Font(self.path, font_size)
    
    def set_color(self, color):
        self.color = color

    def render(self, txt : str):
        self.surface = self.font.render(txt, True, self.color)
        self.rect = self.surface.get_rect()
        return self.rect

    def render(self, txt : str, color):
        self.surface = self.font.render(txt, True, color)
        self.rect = self.surface.get_rect()
        return self.rect
    
    # 位图传送
    def blit_draw(self, screen : pygame.surface.Surface):
        screen.blit(self.surface, self.rect)

    # 位图传送
    def blit(self, screen : pygame.surface.Surface, dest):
        screen.blit(self.surface, dest)
