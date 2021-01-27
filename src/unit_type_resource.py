import pygame


class UnitTypeResource:
    @staticmethod
    def get_icon() -> pygame.Surface:
        raise NotImplementedError()
