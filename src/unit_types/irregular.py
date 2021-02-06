"""
TODO: Доки ко все тута.
"""
from typing import Union

from src.unit_types_resources.irregular import IrregularTypeResource
from src.pow_modifier import POWModifier, POWModifierKind
from src.unit_groups_container import UnitGroupsContainer
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
        return POWModifier(False, 0, current_turn, 0, POWModifierKind.ATTACKING)

    @staticmethod
    def on_defending_against(current_turn: int, groups: UnitGroupsContainer) -> POWModifier:
        return POWModifier(False, 0, current_turn, 0, POWModifierKind.DEFENCIVE)

    @staticmethod
    def get_resource() -> Union[IrregularTypeResource, type]:
        return IrregularTypeResource
