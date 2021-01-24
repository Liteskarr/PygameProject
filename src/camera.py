"""
TODO: Документации.
"""

from typing import Tuple


class Camera:
    """
    Класс игровой камеры.
    """

    def __init__(self, x: int, y: int, width: int, height: int, zoom_factor: float = 1):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._zoom_factor = zoom_factor

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

    def set_zoom_factor(self, zoom_factor: float):
        self._zoom_factor = zoom_factor

    def modify_zoom_factor(self, delta_zf: float):
        self._zoom_factor += delta_zf
        self._zoom_factor = max(0, self._zoom_factor)

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

    def get_rect(self) -> Tuple[int, int, int, int]:
        """
        Получает прямоугольник камеры.
        """
        return self._x, self._y, self._width, self._height

    def get_zoom_factor(self) -> float:
        return self._zoom_factor
