from collections import defaultdict
from typing import Tuple

import pygame

from src.camera import Camera
from src.drawer import Drawer


class GridDrawer(Drawer):
    """
    Отрисовщик сетки на поле.
    """

    def __init__(self, default_color: pygame.Color = None):
        """
        :param default_color: Дефолтный цвет для клеток.
        """
        default_color = pygame.Color('white') if default_color is None else default_color
        self._colors = defaultdict(lambda: default_color)

    def set_grid_color(self, row: int, column: int, color: pygame.Color):
        """
        Устанавливает цвет для данной клетки.
        """
        self._colors[row, column] = color

    def reset_color(self, row: int, column: int):
        """
        Устанавливает дефолтный цвет для данной клетки.
        """
        del self._colors[row, column]

    def render_cell(self,
                    surface: pygame.Surface,
                    cell_size: int,
                    row: int,
                    column: int,
                    camera: Camera,
                    cell_rect: Tuple[int, int, int, int]):
        pygame.draw.rect(surface, self._colors[row, column], cell_rect, 1)
