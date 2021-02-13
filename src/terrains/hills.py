from typing import Union

from src.pow_modifier import POWModifier, NonePOWModifier
from src.terrain import Terrain
from src.terrain_resource import TerrainResource
from src.terrains_resources.hills import HillsResource


class HillTerrain(Terrain):
    @staticmethod
    def get_defencive_bonus() -> POWModifier:
        return NonePOWModifier()

    @staticmethod
    def get_attacking_bonus() -> POWModifier:
        return NonePOWModifier()

    @staticmethod
    def get_movement_cost() -> int:
        return 3

    @staticmethod
    def get_resource() -> Union[TerrainResource, type]:
        return HillsResource
