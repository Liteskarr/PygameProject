from src.pow_modifier import POWModifier, NonePOWModifier
from src.unit_groups_container import UnitGroupsContainer
from src.unit_type import UnitType
from src.unit_type_resource import UnitTypeResource
from src.unit_groups.all import *
from src.units_resources.cuirassier import CuirassierTypeResource


class CuirassierType(UnitType):
    _groups_container = UnitGroupsContainer(CavalryGroup, HeavyGroup)
    _default_pow = 10
    _default_moving_points = 6

    @staticmethod
    def get_groups() -> UnitGroupsContainer:
        return CuirassierType._groups_container

    @staticmethod
    def get_default_pow() -> int:
        return CuirassierType._default_pow

    @staticmethod
    def count_priority() -> int:
        return CuirassierType._groups_container.count_priority()

    @staticmethod
    def get_default_moving_points() -> int:
        return CuirassierType._default_moving_points

    @staticmethod
    def on_attacking_against(current_turn: int, groups: UnitGroupsContainer) -> POWModifier:
        return NonePOWModifier()

    @staticmethod
    def on_defending_against(current_turn: int, groups: UnitGroupsContainer) -> POWModifier:
        return NonePOWModifier()

    @staticmethod
    def is_peaceful() -> bool:
        return False

    @staticmethod
    def use_range_attack() -> bool:
        return False

    @staticmethod
    def get_vision_radius() -> int:
        return 2

    @staticmethod
    def could_move_after_attacking() -> bool:
        return False

    @staticmethod
    def get_resource() -> UnitTypeResource:
        return CuirassierTypeResource
