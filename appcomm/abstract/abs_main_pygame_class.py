from abc import ABC, abstractmethod
import pygame

# main 流程抽象类
class AbsMainPygameListener(ABC):

    @abstractmethod
    def app_handle_event(self, event: pygame.event.Event) -> bool:
        # 子类必须实现的方法
        # 事件处理
        pass

    @abstractmethod
    def app_handle_update(self) -> bool:
        # 子类必须实现的方法
        # 循环体内容处理
        pass

    @abstractmethod
    def app_draw(screen: pygame.surface.Surface):
        pass

    @abstractmethod
    def app_handle_quit(self):
        # 子类必须实现的方法
        # 退出逻辑处理
        pass