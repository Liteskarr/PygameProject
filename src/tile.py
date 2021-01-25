from copy import copy
from typing import Union

from src.biome import Biome, NoneBiome
from src.terrain import Terrain, NoneTerrain


class Tile:
    def __init__(self, biome: Union[Biome, type], terrain: Union[Terrain, type]):
        self._biome = biome
        self._terrain = terrain

    def get_biome(self) -> Biome:
        return copy(self._biome)

    def get_terrain(self) -> Terrain:
        return copy(self._terrain)


class NoneTile(Tile):
    def __init__(self):
        super().__init__(NoneBiome, NoneTerrain)
