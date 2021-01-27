from typing import Tuple

import pygame

from src.drawer import Drawer
from src.game import Game
from src.camera import Camera


class WorldMapDrawer(Drawer):
    def __init__(self, game: Game):
        self._game = game
        self._world_map = game.get_map()

    def render_cell(self,
                    surface: pygame.Surface,
                    cell_size: int,
                    row: int,
                    column: int,
                    camera: Camera,
                    cell_rect: Tuple[int, int, int, int]):
        tile = self._world_map.get_tile(row, column)
        biome_surface = tile.get_biome().get_resource().get_ground_texture()
        biome_surface = pygame.transform.scale(biome_surface, (cell_size, cell_size))
        terrain_surface = tile.get_terrain().get_resource().get_terrain_texture()
        terrain_surface = pygame.transform.scale(terrain_surface, (cell_size, cell_size))
        surface.blit(biome_surface, cell_rect)
        surface.blit(terrain_surface, cell_rect)
