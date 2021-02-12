import pygame

from src.terrain_resource import TerrainResource


class PlainResource(TerrainResource):
    _TEXTURE: pygame.Surface = None

    @staticmethod
    def get_terrain_texture() -> pygame.Surface:
        if PlainResource._TEXTURE is None:
            PlainResource._TEXTURE = pygame.Surface((0, 0))
            PlainResource._TEXTURE = pygame.Surface.convert_alpha(PlainResource._TEXTURE)
            PlainResource._TEXTURE.fill((0, 0, 0, 0))
        return PlainResource._TEXTURE
