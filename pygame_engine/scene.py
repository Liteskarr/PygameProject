"""
Абстракция, позволяющая разделить весь код на несколько логических частей.
Для того, чтобы создать свою собственную сцену унаследуйте
"""

import pygame

from typing import Tuple
from pygame_engine.signal import Signal


class Scene:
    def on_starting(self):
        """
        Вызывается при первом запуске сцены.
        """
        pass

    def on_closing(self):
        """
        Вызывается при открытии другой сцены или закрытии окна.
        """
        pass

    def on_updating(self, delta_time: float):
        """
        Вызывается при каждом обновлении сцены.
        """
        pass

    def on_any_event(self, event: pygame.event.Event):
        """
        Вызывается при любом пришедшем ивенте.
        """
        pass

    def on_userevent(self, event: pygame.event.Event):
        """
        Вызывается, если было поймано пользовательское событие.
        """
        pass

    def on_key_down(self, unicode: str, key: int, mod: int):
        """
        Вызывается, если была опущена кнопка клавиатуры.
        """
        pass

    def on_key_up(self, key: int, mod: int):
        """
        Вызывается, если была поднята кнопка клавиатуры.
        """
        pass

    def on_mouse_motion(self, pos: Tuple[int, int], rel: Tuple[int, int], buttons: Tuple):
        """
        Вызывается, если было произведено движение курсора мыши.
        """
        pass

    def on_mouse_button_down(self, pos: Tuple[int, int], button: int):
        """
        Вызывается, если была опущена кнопка мыши.
        """
        pass

    def on_mouse_button_up(self, pos: Tuple[int, int], button: int):
        """
        Вызывается, если была поднята кнопка мыши.
        """
        pass

    def on_scrolling_up(self, pos: Tuple[int, int]):
        """
        Вызывается, если колесико мыши было проскроллено вверх.
        """
        pass

    def on_scrolling_down(self, pos: Tuple[int, int]):
        """
        Вызывается, если колесико мыши было проскроллено вниз.
        """
        pass
