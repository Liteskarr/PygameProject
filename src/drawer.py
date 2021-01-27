"""
Игровое поле рисуется в несколько этапов, для того, чтобы разделить ответственность
создана эта абстракция.
"""

from typing import Tuple

import pygame

from src.camera import Camera


class Drawer:
    """
    Интерфейс, определяющий поведение рисовальщика объектов по сетке.
    """

    def render_cell(self,
                    surface: pygame.Surface,
                    cell_size: int,
                    row: int,
                    column: int,
                    camera: Camera,
                    cell_rect: Tuple[int, int, int, int]):
        """
        Метод интерфейса, определяющий то, как будет проходить рисование отдельного объекта на клетке.
        :param surface: Поверхность для рисования.
        :param cell_size: Размер одной клетки.
        :param row: Ряд клетки.
        :param column: Столбец клетки.
        :param camera: Используемая в данный момент камера.
        :param cell_rect: Прямоугольник, содержащий область для рисования.
        """
        raise NotImplementedError()
