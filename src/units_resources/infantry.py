import pygame

from src.unit_type_resource import UnitTypeResource


class InfantryTypeResource(UnitTypeResource):
    _ICON = None

    @staticmethod
    def get_icon() -> pygame.Surface:
        if InfantryTypeResource._ICON is None:
            InfantryTypeResource._ICON = pygame.image.load('../data/units/infantry/icon.png')
        return InfantryTypeResource._ICON
