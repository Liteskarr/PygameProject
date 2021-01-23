from copy import copy
from typing import Union

from src.biome import Biome, NoneBiome
from src.terrain import Terrain, NoneTerrain
from src.tiled_resource import TiledResource, NoneTiledResource


class Tile:
    def __init__(self, biome: Union[Biome, type], terrain: Union[Terrain, type], resource: TiledResource):
        self._biome = biome
        self._terrain = terrain
        self._resource = resource

    def get_biome(self) -> Biome:
        return copy(self._biome)

    def get_terrain(self) -> Terrain:
        return copy(self._terrain)

    def get_resource(self) -> TiledResource:
        return copy(self._resource)


class NoneTile(Tile):
    def __init__(self):
        super().__init__(NoneBiome, NoneTerrain, NoneTiledResource())
