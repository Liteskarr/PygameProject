import pygame

from src.unit_type_resource import UnitTypeResource


class CuirassierTypeResource(UnitTypeResource):
    _ICON = None

    @staticmethod
    def get_icon() -> pygame.Surface:
        if CuirassierTypeResource._ICON is None:
            CuirassierTypeResource._ICON = pygame.image.load('../data/units/cuirassier/icon.png')
        return CuirassierTypeResource._ICON
