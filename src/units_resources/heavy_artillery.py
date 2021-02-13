import pygame

from src.unit_type_resource import UnitTypeResource


class HeavyArtilleryTypeResource(UnitTypeResource):
    _ICON = None

    @staticmethod
    def get_icon() -> pygame.Surface:
        if HeavyArtilleryTypeResource._ICON is None:
            HeavyArtilleryTypeResource._ICON = pygame.image.load('../data/units/heavy_artillery/icon.png')
        return HeavyArtilleryTypeResource._ICON
