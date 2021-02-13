import pygame

from src.unit_type_resource import UnitTypeResource


class DragoonTypeResource(UnitTypeResource):
    _ICON = None

    @staticmethod
    def get_icon() -> pygame.Surface:
        if DragoonTypeResource._ICON is None:
            DragoonTypeResource._ICON = pygame.image.load('../data/units/dragoon/icon.png')
        return DragoonTypeResource._ICON
