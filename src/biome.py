from typing import Union

from src.biome_resource import BiomeResource, NoneBiomeResource


class Biome:
    """
    Интерфейс, определяющий поведение биома.
    """

    @staticmethod
    def get_supply_cost() -> int:
        """
        Возвращает цену снабжения при ее распространении в данном биоме.
        """
        raise NotImplementedError()

    @staticmethod
    def get_resource() -> Union[BiomeResource, type]:
        """
        Возвращает класс, содержащий ресурсы, необходимые для визуализации биома.
        """
        raise NotImplementedError()


class NoneBiome(Biome):
    """
    Реализация None-паттерна для интерфейса Biome.
    """

    @staticmethod
    def get_supply_cost() -> int:
        return 1

    @staticmethod
    def get_resource() -> Union[BiomeResource, type]:
        return NoneBiomeResource
