"""
TODO: Доки ко все тута.
"""

from src.pow_modifier import POWModifier, POWModifierKind
from src.unit_group_container import UnitGroupsContainer
from src.unit_groups.infantry import InfantryGroup
from src.unit_groups.light import LightGroup
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
        return POWModifier(POWModifierKind.ATTACKING, False, 0, current_turn, 0)

    @staticmethod
    def on_defending_against(current_turn: int, groups: UnitGroupsContainer) -> POWModifier:
        return POWModifier(POWModifierKind.DEFENCIVE, False, 0, current_turn, 0)
