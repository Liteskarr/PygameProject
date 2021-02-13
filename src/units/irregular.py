"""
TODO: Доки ко всему тута.
"""
from typing import Union

from src.units_resources.irregular import IrregularTypeResource
from src.pow_modifier import POWModifier, POWModifierKind
from src.unit_groups_container import UnitGroupsContainer
from src.unit_groups.all import *
from src.unit_type import UnitType


class IrregularType(UnitType):
    _groups_container = UnitGroupsContainer(InfantryGroup, LightGroup)
    _default_pow = 10
    _moving_points = 5

    @staticmethod
    def get_groups() -> UnitGroupsContainer:
        return IrregularType._groups_container

    @staticmethod
    def get_default_pow() -> int:
        return IrregularType._default_pow

    @staticmethod
    def get_default_moving_points() -> int:
        return IrregularType._moving_points

    @staticmethod
    def on_attacking_against(current_turn: int, groups: UnitGroupsContainer) -> POWModifier:
        return POWModifier(False, 0, current_turn, 0, POWModifierKind.ATTACKING)

    @staticmethod
    def on_defending_against(current_turn: int, groups: UnitGroupsContainer) -> POWModifier:
        return POWModifier(False, 0, current_turn, 0, POWModifierKind.DEFENCIVE)

    @staticmethod
    def get_resource() -> Union[IrregularTypeResource, type]:
        return IrregularTypeResource

    @staticmethod
    def is_peaceful() -> bool:
        return False

    @staticmethod
    def use_range_attack() -> bool:
        return False

    @staticmethod
    def get_vision_radius() -> int:
        return 1

    @staticmethod
    def could_move_after_attacking() -> bool:
        return False

    @staticmethod
    def count_priority() -> int:
        return IrregularType.get_groups().count_priority()
