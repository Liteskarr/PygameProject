import pygame

from src.unit_type_resource import UnitTypeResource


class LightArtilleryTypeResource(UnitTypeResource):
    _ICON = None

    @staticmethod
    def get_icon() -> pygame.Surface:
        if LightArtilleryTypeResource._ICON is None:
            LightArtilleryTypeResource._ICON = pygame.image.load('../data/units/light_artillery/icon.png')
        return LightArtilleryTypeResource._ICON
