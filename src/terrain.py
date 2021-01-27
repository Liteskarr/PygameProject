"""
Интерфейс, определяющий поведение типа местности.
"""

from typing import Union

from src.pow_modifier import POWModifier, NonePOWModifier
from src.terrain_resource import TerrainResource, NoneTerrainResource


class Terrain:
    """
    Интерфейс, описывающий поведение местности на игровой карте.
    """

    @staticmethod
    def get_defencive_bonus() -> POWModifier:
        """
        Возвращает модификатор к защите юнита на карте.
        """
        raise NotImplementedError()

    @staticmethod
    def get_attacking_bonus() -> POWModifier:
        """
        Возвращает модификатор к атаке юнита на карте.
        """
        raise NotImplementedError()

    @staticmethod
    def get_movement_cost() -> int:
        """
        Возвращает стоимость пересечения данной местности.
        """
        raise NotImplementedError()

    @staticmethod
    def get_resource() -> Union[TerrainResource, type]:
        """
        Возвращает ресурсы для визуализации типа местности на карте.
        """
        raise NotImplementedError()


class NoneTerrain(Terrain):
    """
    Реализация None-паттерна для класса Terrain.
    """

    @staticmethod
    def get_defencive_bonus() -> POWModifier:
        return NonePOWModifier()

    @staticmethod
    def get_attacking_bonus() -> POWModifier:
        return NonePOWModifier()

    @staticmethod
    def get_movement_cost() -> int:
        return 1

    @staticmethod
    def get_resource() -> Union[TerrainResource, type]:
        return NoneTerrainResource
