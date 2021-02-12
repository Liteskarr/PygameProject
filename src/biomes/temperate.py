from typing import Union

from src.biome import Biome
from src.biome_resource import BiomeResource
from src.biomes_resources.temperate import TemperateBiomeResource


class TemperateBiome(Biome):
    @staticmethod
    def get_supply_cost() -> int:
        return 2

    @staticmethod
    def get_resource() -> Union[BiomeResource, type]:
        return TemperateBiomeResource
