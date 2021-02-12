from typing import Union

from src.terrains_resources.plain import PlainResource
from src.pow_modifier import POWModifier, NonePOWModifier
from src.terrain import Terrain
from src.terrain_resource import TerrainResource


class PlainTerrain(Terrain):
    @staticmethod
    def get_defencive_bonus() -> POWModifier:
        return NonePOWModifier()

    @staticmethod
    def get_attacking_bonus() -> POWModifier:
        return NonePOWModifier()

    @staticmethod
    def get_movement_cost() -> int:
        return 2

    @staticmethod
    def get_resource() -> Union[TerrainResource, type]:
        return PlainResource
