import pygame

from src.terrain_resource import TerrainResource


class HillsResource(TerrainResource):
    _TEXTURE: pygame.Surface = None

    @staticmethod
    def get_terrain_texture() -> pygame.Surface:
        if HillsResource._TEXTURE is None:
            HillsResource._TEXTURE = pygame.image.load('../data/terrains/hills.png')
        return HillsResource._TEXTURE
