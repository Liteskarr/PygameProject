import pygame

from src.unit_type_resource import UnitTypeResource


class IrregularTypeResource(UnitTypeResource):
    _ICON = None

    @staticmethod
    def get_icon() -> pygame.Surface:
        if IrregularTypeResource._ICON is None:
            IrregularTypeResource._ICON = pygame.image.load('../data/units/irregular/icon.png')
        return IrregularTypeResource._ICON
