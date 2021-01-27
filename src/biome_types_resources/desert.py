import pygame

from src.biome_resource import BiomeResource


class DesertBiomeResource(BiomeResource):
    _TEXTURE = None

    @staticmethod
    def get_ground_texture() -> pygame.Surface:
        if DesertBiomeResource._TEXTURE is None:
            DesertBiomeResource._TEXTURE = pygame.image.load('../data/biomes/desert/texture.png')
        return DesertBiomeResource._TEXTURE
