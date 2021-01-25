"""
TODO: Документация
"""

from copy import copy
from typing import Tuple
from collections import namedtuple

from noise import pnoise3

from random import randint

from src.tile import Tile, NoneTile
from src.terrain import get_terrain
from src.biome import get_biome

class WorldMap:
    """

    """

    def __init__(self, width: int, height: int, looped: Tuple[bool, bool] = None, fill: Tile = None):
        self._width = width
        self._height = height
        self._h_looped, self._v_looped = looped if looped is not None else (False, False)
        fill = NoneTile if fill is None else fill
        self._tiles = [[copy(fill) for c in range(self._width)] for c in range(self._height)]

    def get_size(self) -> Tuple[int, int]:
        """

        :return:
        """
        return self._width, self._height

    def apply_looping(self, row: int, column: int) -> Tuple[int, int]:
        """

        :param row:
        :param column:
        :return:
        """
        row = row % self._height if self._v_looped else row
        column = column % self._width if self._h_looped else column
        return row, column

    def set_tile(self, row: int, column: int, tile: Tile):
        """

        :param row:
        :param column:
        :param tile:
        :return:
        """
        row, column = self.apply_looping(row, column)
        self._tiles[row][column] = copy(tile)

    def get_tile(self, row: int, column: int) -> Tile:
        """
        Получить тайл, который находится на данной координате.
        :param row:
        :param column:
        :return:
        """
        row, column = self.apply_looping(row, column)
        return copy(self._tiles[row][column])

    def generate(self, biome_seed = random.randint(1, 0xffffff), terrain_seed = random.randint(1, 0xffffff)):
            for x in range(self._width):
                for y in range(self._height):
                    self.gen_biome = int((pnoise3(float(x + 50) * 0.3, float(y + 50) * 0.3,
                                       biome_seed) + 1) * 128)
                    self.gen_terrain = int((pnoise3(float(x + 50) * 0.3, float(y + 50) * 0.3,
                                       terrain_seed) + 1) * 128)
                    self._tiles[x][y] = Tile(get_biome(gen_biome), get_terrain(gen_terrain))
