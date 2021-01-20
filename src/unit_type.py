"""
TODO: Написать то, зачем это нужно.
"""

from src.pow_modifier import POWModifier
from src.unit_group_container import UnitGroupsContainer


class UnitType:
    """
    Описывает тип юнита на игровом поле.
    Является статическим классом.
    """

    @staticmethod
    def get_groups() -> UnitGroupsContainer:
        """
        Возвращает группы, к которым относится тип юнита.
        """
        raise NotImplementedError()

    @staticmethod
    def get_default_pow() -> int:
        """
        Возвращает дефолтное количество очков POW для данного типа юнитов.
        """
        raise NotImplementedError()

    @staticmethod
    def get_default_moving_points() -> int:
        """
        Возвращает дефолтное количество очков движения для данного типа юитов.
        """
        raise NotImplementedError()

    @staticmethod
    def on_attacking_against(current_turn: int, groups: UnitGroupsContainer) -> POWModifier:
        """
        Возвращает модификатор к POW для данного юнита в атаке против юнита, имеющего данные группы.
        """
        raise NotImplementedError()

    @staticmethod
    def on_defending_against(current_turn: int, groups: UnitGroupsContainer) -> POWModifier:
        """
        Возвращает модификатор к POW для данного юнита в защите против юнита, имеющего данные группы.
        """
        raise NotImplementedError()
