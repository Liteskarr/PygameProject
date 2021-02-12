import pygame

from src.biome_resource import BiomeResource


class TemperateBiomeResource(BiomeResource):
    _TEXTURE = None

    @staticmethod
    def get_ground_texture() -> pygame.Surface:
        if TemperateBiomeResource._TEXTURE is None:
            TemperateBiomeResource._TEXTURE = pygame.image.load('../data/biomes/temperate/texture.png')
        return TemperateBiomeResource._TEXTURE
