"""
Интерфейс, определяющий поведение биома.
"""

from src.pow_modifier import POWModifier


class Biome:
    @staticmethod
    def get_supply_cost() -> int:
        raise NotImplementedError()


class NoneBiome(Biome):
    @staticmethod
    def get_supply_cost() -> int:
        return 1

def get_biome(x):
	pass