import pygame


class BiomeResource:
    """
    Интерфейс, содержащий методы для получения ресурсов биома.
    """

    @staticmethod
    def get_ground_texture() -> pygame.Surface:
        """
        Возвращает текстуру почвы биома.
        """
        raise NotImplementedError()


class NoneBiomeResource(BiomeResource):
    """
    Реализация None-паттерна для класса BiomeResource.
    """

    _TEXTURE = None

    @staticmethod
    def get_ground_texture() -> pygame.Surface:
        if NoneBiomeResource._TEXTURE is None:
            NoneBiomeResource._TEXTURE = pygame.image.load('../data/textures/empty_texture.png')
            NoneBiomeResource._TEXTURE = pygame.Surface.convert_alpha(NoneBiomeResource._TEXTURE)
            NoneBiomeResource._TEXTURE.set_alpha(128)
        return NoneBiomeResource._TEXTURE
