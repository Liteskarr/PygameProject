"""
Интерфейс, определяющий поведение типа местности.
"""


class Terrain:
    @staticmethod
    def get_attacking_bonus():
        raise NotImplementedError()

    @staticmethod
    def get_movement_cost():
        raise NotImplementedError()
