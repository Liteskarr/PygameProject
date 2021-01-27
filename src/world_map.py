from copy import copy
from typing import Tuple

from src.tile import Tile, NoneTile


class WorldMap:
    """
    Класс карты игрового мира.
    """

    def __init__(self, width: int, height: int, fill: Tile = None):
        self._width = width
        self._height = height
        fill = NoneTile() if fill is None else fill
        self._tiles = [[copy(fill) for c in range(self._width)] for c in range(self._height)]

    def get_size(self) -> Tuple[int, int]:
        """
        Возвращает размеры игрового поля.
        """
        return self._width, self._height

    def set_tile(self, row: int, column: int, tile: Tile):
        """
        Устанавливает на клетку новый тайл.
        """
        self._tiles[row][column] = copy(tile)

    def get_tile(self, row: int, column: int) -> Tile:
        """
        Возвращает тайл, который находится на данной координате.
        """
        return copy(self._tiles[row][column])
