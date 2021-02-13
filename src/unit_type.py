"""
TODO: Написать то, зачем это нужно.
"""

from src.pow_modifier import POWModifier
from src.unit_type_resource import UnitTypeResource
from src.unit_groups_container import UnitGroupsContainer


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
    def count_priority() -> int:
        """
        Возвращает приоритет юнитов в клетке.
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

    @staticmethod
    def is_peaceful() -> bool:
        """
        Определяет, является ли данный юнит мирным.
        """
        raise NotImplementedError()

    @staticmethod
    def use_range_attack() -> bool:
        """
        Определяет, является ли атака юнита дистанционной.
        """
        raise NotImplementedError()

    @staticmethod
    def get_vision_radius() -> int:
        """
        Возвращает радиус обзора данного типа юнитов.
        """
        raise NotImplementedError()

    @staticmethod
    def could_move_after_attacking() -> bool:
        """
        Определяет, может ли юнит передвигаться после атаки.
        """
        raise NotImplementedError()

    @staticmethod
    def get_resource() -> UnitTypeResource:
        """
        Возвращает класс ресурсов типа юнита.
        """
        raise NotImplementedError()
