"""
TODO: Написать то, зачем это нужно.
"""

from math import ceil, exp
from typing import Tuple, List

from pygame_engine.signal import Signal

from src.pow_modifier import POWModifier
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

    def set_unit(self, pos: Tuple[int, int], unit: Unit):
        pass
