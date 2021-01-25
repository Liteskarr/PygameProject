"""
Интерфейс, определяющий поведение типа местности.
"""

from src.pow_modifier import POWModifier, NonePOWModifier


class Terrain:
    @staticmethod
    def get_defencive_bonus() -> POWModifier:
        raise NotImplementedError()

    @staticmethod
    def get_attacking_bonus() -> POWModifier:
        raise NotImplementedError()

    @staticmethod
    def get_movement_cost() -> int:
        raise NotImplementedError()


class NoneTerrain(Terrain):
    @staticmethod
    def get_defencive_bonus() -> POWModifier:
        return NonePOWModifier()

    @staticmethod
    def get_attacking_bonus() -> POWModifier:
        return NonePOWModifier()

    @staticmethod
    def get_movement_cost() -> int:
        return 1

def get_terrain(x):
    pass