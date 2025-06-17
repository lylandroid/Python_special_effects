import pygame
import os

class SoundHelper:

    is_pause = False

    def __init__(self, _file_, uri: str):
        super().__init__()
        # 初始化音频模块 (通常在 pygame.init() 后)
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        if _file_ is not None:
            dir = os.path.dirname(_file_)
            self.path = os.path.join(dir, uri)
        else:
            self.path = uri
            
        self.channel  = None
        self.sound = None
        print(f"SoundHelper.path = {self.path}")
    
    def get_sound(self):
        if self.sound is None:
            self.sound = pygame.mixer.Sound(self.path)
            print(f"SoundHelper.get_sound() new sound = {self.sound}")
        return self.sound
    
    def play(self, volume = 0.5, loops = 0):
        if self.channel is None or not self.channel.get_busy():
            self.channel = self.get_sound().play(loops=loops)
            print(f"self.channel = {self.channel}")
            self.channel.set_volume(volume)
        elif self.is_pause:
            self.channel.unpause()

    def is_playing(self) -> bool:
        return self.channel and self.channel.get_busy() and not self.is_pause
    
    def pause(self):
        if self.channel.get_busy():
            self.is_pause = True
            self.channel.pause()

    def stop(self):
        if self.channel is not None and self.channel.get_busy():
            self.channel.stop()
            self.channel = None


                