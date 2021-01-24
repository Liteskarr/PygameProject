"""
TODO: Документации.
"""

from typing import Tuple


class Camera:
    """
    Класс игровой камеры.
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    def intersect_with_rect(self, rect: Tuple[int, int, int, int]) -> bool:
        """
        Проверяет пересечение обзора камеры с другим прямоугольником.
        :param rect: Другой прямоугольник.
        """
        x, y, width, height = rect
        return not(self._x >= x + width or
                   x >= self._x + self._width or
                   self._y >= y + height or
                   y >= self._y + self._height)

    def contains_point(self, x: int, y: int) -> bool:
        """
        Лежит ли точка в игровом мире в обзоре камеры.
        """
        return self._x <= x <= self._x + self._width and self._y <= y <= self._y + self._height

    def move(self, x: int, y: int):
        """
        Двигает камеру на координаты X;Y.
        """
        self._x = x
        self._y = y

    def move_at_vector(self, x: int, y: int):
        """
        Двигает камеру на вектор X;Y.
        """
        self._x += x
        self._y += y

    def resize(self, width: int, height: int):
        """
        Изменяет размеры игровой камеры.
        """
        self._width = width
        self._height = height

    def resize_at_vector(self, width: int, height: int):
        """
        Изменяет размеры игровой камеры на вектор.
        """
        self._width += width
        self._height += height

    def mouse_pos_to_world_pos(self, x: int, y: int) -> Tuple[int, int]:
        """
        Преобразует координаты мыши в мировые координаты.
        """
        return self._x + x, self._y + y

    def world_pos_to_mouse_pos(self, x: int, y: int) -> Tuple[int, int]:
        """
        Преобразует мировые координаты в координаты на экране.
        """
        return x - self._x, y - self._y
