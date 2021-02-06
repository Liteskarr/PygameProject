"""
Точка входа в программу.
"""

import pygame

from pygame_engine.engine import Engine
from pygame_engine.window import Window

from src.main_menu_scene import MainMenuScene
from src.game_scene import GameScene


def main():
    Window.init(1280, 720, 'TBMM')
    Engine.target_fps = 60
    Engine.set_scene(GameScene('test'))
    Engine.run()


if __name__ == '__main__':
    pygame.init()
    main()
