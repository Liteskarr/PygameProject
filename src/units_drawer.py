from typing import Tuple

import pygame

from src.drawer import Drawer
from src.game import Game
from src.camera import Camera


class UnitsDrawer(Drawer):
    def __init__(self, game: Game):
        self._game = game
        self._units_manager = self._game.get_units_manager()

    def render_cell(self,
                    surface: pygame.Surface,
                    cell_size: int,
                    row: int,
                    column: int,
                    camera: Camera,
                    cell_rect: Tuple[int, int, int, int]):
        unit = self._units_manager.get_unit(row, column)
        if unit is None:
            return

        major_color = unit.get_owner().major_color
        minor_color = unit.get_owner().minor_color

        unit_surface = pygame.Surface((int(cell_size / 2), int(cell_size / 2)))
        unit_surface = pygame.Surface.convert_alpha(unit_surface)
        unit_surface.fill((0, 0, 0, 0))

        circle_rect = (cell_rect[0] + 1, cell_rect[1] + 1, int(cell_size - 2) // 2, int(cell_size - 2) // 2)
        pygame.draw.ellipse(surface, major_color, circle_rect)
        pygame.draw.ellipse(surface, minor_color, circle_rect, int(cell_size / 40))

        unit_icon = unit.get_resource().get_icon()
        unit_icon = pygame.transform.scale(unit_icon, (int(cell_size / 2), int(cell_size / 2)))
        surface.blit(unit_icon, cell_rect)
