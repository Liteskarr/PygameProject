"""
Сцена, содержащая игровой процесс.
"""

from typing import Tuple

import pygame
from src.pygame_engine.scene import Scene
from src.pygame_engine.window import Window
from src.cities_component import CitiesComponent
from src.fog_component import FogComponent

from src.game import Game
from src.camera import Camera
from src.grid_component import GridComponent
from src.judge_component import JudgeComponent
from src.player import Player

from src.world_map_component import WorldMapComponent
from src.units_component import UnitsComponent
from src.input_component import InputComponent
from src.gui_component import GUIComponent


player1 = Player(major_color=pygame.Color('green'), minor_color=pygame.Color('red'), name='player1')
player2 = Player(major_color=pygame.Color('black'), minor_color=pygame.Color('blue'), name='player2')


class GameScene(Scene):
    def __init__(self, saving: str):
        self._saving = saving
        self.main_menu_game_scene_cls = None

    def on_starting(self):
        window_size = Window.get_size()
        self.screen_surface = Window.get_screen_surface()

        self.main_camera = Camera(0, 0, *window_size)

        self.game = Game()
        self.game.main_menu_scene_cls = self.main_menu_game_scene_cls
        self.game.init_component(GUIComponent())
        self.game.init_component(WorldMapComponent())
        self.game.init_component(UnitsComponent())
        self.game.init_component(GridComponent())
        self.game.init_component(CitiesComponent())
        self.game.init_component(InputComponent())
        self.game.init_component(FogComponent())
        self.game.init_component(JudgeComponent())
        self.game.set_camera(self.main_camera)
        self.game.load(self._saving)

    def on_updating(self, delta_time: float):
        self.delta_time = delta_time
        Window.clear_screen()
        self.game.update(delta_time)
        self.game.render_all(self.screen_surface)

    def on_any_event(self, event: pygame.event.Event):
        self.game.handle_event(event)

    def on_mouse_motion(self, pos: Tuple[int, int], rel: Tuple[int, int], buttons: Tuple):
        if buttons[2]:
            self.main_camera.move_at_vector(*map(lambda x: -x, rel))

    def on_scrolling_up(self, pos: Tuple[int, int]):
        self.game.set_cell_size(self.game.get_cell_size() + 3)

    def on_scrolling_down(self, pos: Tuple[int, int]):
        self.game.set_cell_size(self.game.get_cell_size() - 3)
