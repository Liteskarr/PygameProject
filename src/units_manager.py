"""
TODO: Написать то, зачем это нужно.
"""

from math import ceil, exp
from typing import Tuple

from pygame_engine.signal import Signal

from src.pow_modifier import POWModifier
from src.unit import Unit


def get_damage(unit_pow: int, enemy_pow: int) -> int:
    pow_difference = unit_pow - enemy_pow
    base = enemy_pow
    modifier = exp(0.1 * pow_difference)
    k = 3
    return ceil(base + modifier + k) // k


class UnitsManager:
    def __init__(self, world_map):
        self._init_signals()

    def _init_signals(self):
        pass

    def unit_could_move(self, unit_pos: Tuple[int, int], target_pos: Tuple[int, int]) -> bool:
        pass

    def unit_could_attack(self, unit_pos: Tuple[int, int], enemy_pos: Tuple[int, int]) -> bool:
        pass

    def move_unit(self, unit_pos: Tuple[int, int], target_pos: Tuple[int, int]):
        pass

    def attack_unit(self, unit_pos: Tuple[int, int], enemy_pos: Tuple[int, int]):
        pass

    def swap_units(self, unit_pos: Tuple[int, int], another_unit_pos: Tuple[int, int]):
        pass

    def get_unit_pow(self, unit_pos: Tuple[int, int]) -> Tuple[int, List[POWModifier]]:
        pass
