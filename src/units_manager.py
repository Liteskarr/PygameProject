"""
TODO: Написать то, зачем это нужно.
"""

from math import ceil, exp
from typing import Tuple, List

from src.unit import Unit
from src.world_map import WorldMap


def get_damage(unit_pow: int, enemy_pow: int) -> int:
    pow_difference = unit_pow - enemy_pow
    base = enemy_pow
    modifier = exp(0.1 * pow_difference)
    k = 3
    return ceil(base + modifier + k) // k


class UnitsManager:
    def __init__(self, world_map: WorldMap):
        self._world_map = world_map
        self._units = {}
        self._init_signals()

    def _init_signals(self):
        pass

    def get_all_units(self) -> List[Tuple[int, int, Unit]]:
        return list(map(lambda unit: unit[0] + (unit[1],), self._units.items()))

    def set_unit(self, row: int, column: int, unit: Unit):
        self._units[row, column] = unit

    def get_unit(self, row: int, column: int) -> Unit:
        return self._units[row, column] if (row, column) in self._units else None

    def delete_unit(self, row: int, column: int):
        del self._units[row, column]

    def move_unit(self, from_row: int, from_column: int, to_row: int, to_column: int):
        self.set_unit(to_row, to_column, self.get_unit(from_row, from_column))
        self.delete_unit(from_row, from_column)
