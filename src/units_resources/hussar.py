import pygame

from src.unit_type_resource import UnitTypeResource


class HussarTypeResource(UnitTypeResource):
    _ICON = None

    @staticmethod
    def get_icon() -> pygame.Surface:
        if HussarTypeResource._ICON is None:
            HussarTypeResource._ICON = pygame.image.load('../data/units/hussar/icon.png')
        return HussarTypeResource._ICON
