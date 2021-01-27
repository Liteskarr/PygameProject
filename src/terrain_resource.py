import pygame


class TerrainResource:
    @staticmethod
    def get_terrain_texture() -> pygame.Surface:
        raise NotImplementedError()


class NoneTerrainResource(TerrainResource):
    _TEXTURE = None

    @staticmethod
    def get_terrain_texture() -> pygame.Surface:
        if NoneTerrainResource._TEXTURE is None:
            NoneTerrainResource._TEXTURE = pygame.Surface((200, 200))
            NoneTerrainResource._TEXTURE = pygame.Surface.convert_alpha(NoneTerrainResource._TEXTURE)
            NoneTerrainResource._TEXTURE.set_alpha(0)
        return NoneTerrainResource._TEXTURE
