"""
Сцена, содержащая игровой процесс.
"""

from typing import Tuple

import pygame

from pygame_engine.scene import Scene
from pygame_engine.engine import Engine
from pygame_engine.window import Window

from src.tile import Tile
from src.game import Game
from src.unit import Unit
from src.camera import Camera
from src.world_map import WorldMap
from src.terrain import NoneTerrain
from src.units_drawer import UnitsDrawer
from src.units_manager import UnitsManager
from src.world_map_drawer import WorldMapDrawer
from src.biome_types.desert import DesertBiome
from src.grid_drawer import GridDrawer
from src.player import Player, God
from src.drawers_store import DrawersStore

from src.unit_types.irregular import IrregularType


admin = God(major_color=pygame.Color('black'), minor_color=pygame.Color('gold'), name='liteskarr')


class GameScene(Scene):
    def on_starting(self):
        window_size = Window.get_size()
        self.screen_surface = Window.get_screen_surface()

        self.main_camera = Camera(0, 0, *window_size)

        self.game = Game()

        self.world_size = 10, 10
        self.world_map = WorldMap(*window_size, fill=Tile(DesertBiome, NoneTerrain))
        self.game.set_map(self.world_map)

        self.units_manager = UnitsManager(self.world_map)
        self.units_manager.set_unit(0, 0, Unit(IrregularType, admin))
        self.game.set_units_manager(self.units_manager)

        self.cell_size = 60
        self.drawers_store = DrawersStore(self.world_size[0],
                                          self.world_size[1],
                                          self.cell_size,
                                          self.main_camera,
                                          [
                                              WorldMapDrawer(self.game),
                                              UnitsDrawer(self.game),
                                              GridDrawer(pygame.Color('white'))
                                          ])
        self.delta_time = 0

    def on_updating(self, delta_time: float):
        self.delta_time = delta_time
        Window.clear_screen()
        self.drawers_store.render_at(self.screen_surface)
        Window.set_title(str(self.delta_time_s))

    def on_mouse_button_down(self, pos: Tuple[int, int], button: int):
        if button == 1:
            pass
        elif button == 3:
            pass

    def on_mouse_motion(self, pos: Tuple[int, int], rel: Tuple[int, int], buttons: Tuple):
        if buttons[2] == 1:
            self.main_camera.move_at_vector(*map(lambda x: -x, rel))
