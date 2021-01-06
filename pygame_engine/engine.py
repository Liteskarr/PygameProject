"""
Главный статический класс, отвечащий за связывание сцен и API pygame'а.
"""

import pygame

from pygame_engine.window import Window
from pygame_engine.scene import Scene


class Engine:
    target_fps: int = 60
    running: bool = False
    clock: pygame.time.Clock = pygame.time.Clock()
    _current_scene: Scene

    @staticmethod
    def set_scene(new_scene: Scene):
        """
        Устанавливат текущую сцену.
        """
        Engine._current_scene = new_scene
        Engine._current_scene.on_starting()

    @staticmethod
    def update():
        """
        Отвечает за логику каждого игрового кадра.
        """
        Window.clear_screen()
        for event in pygame.event.get():
            Engine._current_scene.on_any_event(event)
            if event.type == pygame.QUIT:
                Engine._current_scene.on_closing()
                Engine.running = False
                break
            elif event.type == pygame.USEREVENT:
                Engine._current_scene.on_userevent(event)
            elif event.type == pygame.MOUSEMOTION:
                Engine._current_scene.on_mouse_motion(event.pos, event.rel, event.buttons)
            elif event.type == pygame.MOUSEBUTTONUP:
                Engine._current_scene.on_mouse_button_up(event.pos, event.button)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Engine._current_scene.on_mouse_button_down(event.pos, event.button)
                if event.button == 4:
                    Engine._current_scene.on_scrolling_up(event.pos)
                elif event.button == 5:
                    Engine._current_scene.on_scrolling_down(event.pos)
            elif event.type == pygame.KEYUP:
                Engine._current_scene.on_key_up(event.key, event.mod)
            elif event.type == pygame.KEYDOWN:
                Engine._current_scene.on_key_down(event.unicode, event.key, event.mod)
        Engine._current_scene.on_updating(Engine.clock.tick(Engine.target_fps))
        pygame.display.update()

    @staticmethod
    def run():
        """
        Запускает игру.
        """
        Engine.running = True
        while Engine.running:
            Engine.update()
