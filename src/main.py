import pygame

from pygame_engine.engine import Engine
from pygame_engine.window import Window

from src.game_scene import GameScene


def main():
    Window.init(800, 600, 'TBMM')
    Engine.set_scene(GameScene())
    Engine.run()


if __name__ == '__main__':
    pygame.init()
    main()
