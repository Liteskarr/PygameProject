"""
Сцена, содержащая игровой процесс.
"""

from typing import Tuple

import pygame
from pygame_engine.scene import Scene
from pygame_engine.window import Window
from src.fog_component import FogComponent

from src.game import Game
from src.camera import Camera
from src.grid_component import GridComponent
from src.player import God, Player
from src.unit import Unit
from src.unit_types.irregular import IrregularType

from src.world_map_component import WorldMapComponent
from src.units_component import UnitsComponent
from src.input_component import InputComponent
from src.gui_component import GUIComponent


player1 = Player(major_color=pygame.Color('green'), minor_color=pygame.Color('red'), name='player1')
player2 = Player(major_color=pygame.Color('black'), minor_color=pygame.Color('blue'), name='player2')


class GameScene(Scene):
    def __init__(self, saving: str):
        self._saving = saving

    def on_starting(self):
        window_size = Window.get_size()
        self.screen_surface = Window.get_screen_surface()

        self.main_camera = Camera(0, 0, *window_size)

        self.game = Game()
        self.game.init_component(WorldMapComponent())
        self.game.init_component(UnitsComponent())
        self.game.init_component(GUIComponent())
        self.game.init_component(GridComponent())
        self.game.init_component(InputComponent())
        self.game.init_component(FogComponent())
        self.game.set_camera(self.main_camera)
        self.game.load(self._saving)
        uc = self.game.get_component(UnitsComponent)
        uc.add_unit(0, 1, Unit(IrregularType, player1))
        uc.add_unit(0, 0, Unit(IrregularType, player2))
        uc.add_unit(0, 0, Unit(IrregularType, player2))

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
