"""
Интерфейс, определяющий поведение типа местности.
"""

from src.pow_modifier import POWModifier


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
