"""
Многие этапы отрисовки повторяются, такие как, например, обход возможных клеток для отрисовки.
Этот класс реализует их и вызывает объекты, которые занимаются отрисовкой.
"""

from typing import List
from math import ceil

import pygame

from src.drawer import Drawer
from src.camera import Camera


class DrawersStore:
    """
    Класс-хранитель для объектов класса Drawer.
    """

    def __init__(self,
                 width: int,
                 height: int,
                 cell_size: int,
                 camera: Camera,
                 drawers: List[Drawer]):
        """
        :param width: Ширина сетки.
        :param height: Высота сетки.
        :param cell_size: Базовый размер клетки.
        :param camera: Камера.
        :param drawers: Список отрисовщиков.
        """
        self._width = width
        self._height = height
        self._cell_size = cell_size
        self._camera = camera
        self._drawers = drawers

    def render_at(self, surface: pygame.Surface):
        """
        Рисует игровое поле на поверхность surface, учитывая камеру и требуемый размер клеток.
        :param surface: Поверхность, на которую происходить отрисовка.
        """
        cx, cy, cw, ch = self._camera.get_rect()
        from_row = max(cy // self._cell_size, 0)
        from_column = max(cx // self._cell_size, 0)
        cell_size = self._cell_size * self._camera.get_zoom_factor()
        for r in range(from_row, self._height):
            dirty_flag = True
            for c in range(from_column, self._width):
                cell_rect = tuple(map(lambda x: int(ceil(x)),
                                      (c * cell_size - cx, r * cell_size - cy, cell_size, cell_size)))
                raw_cell_rect = (cell_rect[0] + cx, cell_rect[1] + cy) + cell_rect[2:]
                if self._camera.intersect_with_rect(raw_cell_rect):
                    dirty_flag = False
                    for drawer in self._drawers:
                        drawer.render_cell(surface, int(cell_size), r, c, self._camera, cell_rect)
                else:
                    break
            if dirty_flag:
                break
