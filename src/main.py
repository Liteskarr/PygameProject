"""
Точка входа в программу.
"""

import pygame

from src.pygame_engine.engine import Engine
from src.pygame_engine.window import Window

from src.main_menu_scene import MainMenuScene


def main():
    Window.init(1280, 720, 'TBMM')
    Window.set_icon(pygame.image.load('../data/textures/icon.jpg'))
    Engine.target_fps = 60
    Engine.set_scene(MainMenuScene())
    Engine.run()


if __name__ == '__main__':
    pygame.init()
    main()
