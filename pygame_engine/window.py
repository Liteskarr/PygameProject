"""
Удобное взаимодействие с окном приложения без использования pygame напрямую
Реализует все необходимые функции.
"""

from typing import Tuple

import pygame


class Window:
    fill_color: pygame.Color = pygame.Color('black')

    @staticmethod
    def init(width: int, height: int, title: str = 'Game', flags=0):
        pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption(title)

    @staticmethod
    def toggle_fullscreen():
        pygame.display.toggle_fullscreen()

    @staticmethod
    def set_icon(icon_surface: pygame.Surface):
        pygame.display.set_icon(icon_surface)

    @staticmethod
    def set_size(width: int, height: int):
        pygame.display.set_mode((width, height))

    @staticmethod
    def get_size() -> Tuple[int, int]:
        return pygame.display.get_window_size()

    @staticmethod
    def set_title(title: str):
        pygame.display.set_caption(title)

    @staticmethod
    def get_title() -> str:
        return pygame.display.get_caption()[0]

    @staticmethod
    def get_screen_surface() -> pygame.Surface:
        return pygame.display.get_surface()

    @staticmethod
    def clear_screen():
        Window.get_screen_surface().fill(Window.fill_color)

    @staticmethod
    def update(rect: pygame.Rect = None):
        pygame.display.update(rect)
