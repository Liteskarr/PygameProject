from copy import copy
from typing import Tuple, List

import pygame

from src.data_packet_types.all import (RequestMovementCost, ShapeUpdated)
from src.data_packet import DataPacket
from src.game_component import GameComponent
from src.camera import Camera
from src.tile import Tile, NoneTile


class WorldMapComponent(GameComponent):
    """
    Класс карты игрового мира.
    """
    def __init__(self):
        self._width: int = 0
        self._height: int = 0
        self._tiles: List[List[Tile]]

    def handle_packet(self, packet: DataPacket):
        if packet.type is RequestMovementCost:
            self.handle_cell_movement_getting_request(packet)
        elif packet.type is ShapeUpdated:
            self.handle_shape_updating(packet)

    def handle_shape_updating(self, packet: DataPacket):
        self._width, self._height = packet.args
        self._tiles = [[copy(NoneTile()) for column in range(self._width)] for row in range(self._height)]

    def handle_cell_movement_getting_request(self, packet: DataPacket):
        for row in range(self._height):
            for column in range(self._width):
                packet.response_function(row, column, self.get_tile(row, column).get_terrain().get_movement_cost())

    def get_shape(self) -> Tuple[int, int]:
        """
        Возвращает размеры игрового поля.
        """
        return self._width, self._height

    def set_tile(self, row: int, column: int, tile: Tile):
        """
        Устанавливает на клетку новый тайл.
        """
        self._tiles[row][column] = copy(tile)

    def get_tile(self, row: int, column: int) -> Tile:
        """
        Возвращает тайл, который находится на данной координате.
        """
        return copy(self._tiles[row][column])

    def is_valid_tile(self, row: int, column: int) -> bool:
        return 0 <= row < self._height and 0 <= column < self._width

    def render_cell(self,
                    surface: pygame.Surface,
                    cell_size: int,
                    row: int,
                    column: int,
                    camera: Camera,
                    cell_rect: pygame.Rect):
        tile = self.get_tile(row, column)
        biome_surface = tile.get_biome().get_resource().get_ground_texture()
        biome_surface = pygame.transform.scale(biome_surface, (cell_size, cell_size))
        terrain_surface = tile.get_terrain().get_resource().get_terrain_texture()
        terrain_surface = pygame.transform.scale(terrain_surface, (cell_size, cell_size))
        surface.blit(biome_surface, cell_rect)
        surface.blit(terrain_surface, cell_rect)
