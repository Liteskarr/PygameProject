from typing import Tuple

import pygame

from pygame_engine.scene import Scene
from pygame_engine.engine import Engine
from pygame_engine.window import Window

from src.game import Game
from src.camera import Camera
from src.map_drawer import MapDrawer


class GameScene(Scene):
    def on_starting(self):
        self.main_camera = Camera(100, 0, *Window.get_size())
        self.game = Game()
        self.map_drawer = MapDrawer(self.game, self.main_camera, 60)
        self.delta_time = 0

    def on_updating(self, delta_time: float):
        self.delta_time = delta_time
        Window.clear_screen()
        self.game.update()
        self.map_drawer.render_at(Window.get_screen_surface())

    def on_mouse_motion(self, pos: Tuple[int, int], rel: Tuple[int, int], buttons: Tuple):
        if buttons[2] == 1:
            self.main_camera.move_at_vector(*map(lambda x: -x, rel))

    def on_scrolling_up(self, pos: Tuple[int, int]):
        self.main_camera.modify_zoom_factor(-0.01 * self.delta_time)

    def on_scrolling_down(self, pos: Tuple[int, int]):
        self.main_camera.modify_zoom_factor(0.01 * self.delta_time)
