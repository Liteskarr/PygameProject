import pygame

from src.camera import Camera
from src.data_packet import DataPacket
from src.data_packets.all import (UnitVisionMapUpdated,
                                  NextTurn,
                                  CityVisionMapUpdated)
from src.game_component import GameComponent


class FogComponent(GameComponent):
    def __init__(self):
        self._FOG_TEXTURE = pygame.image.load('../data/textures/fog.png')
        self._units_visible_cells: set = set()
        self._city_visible_cells: set = set()

    def handle_packet(self, packet: DataPacket):
        if packet.type is UnitVisionMapUpdated:
            self._units_visible_cells = packet.args
        elif packet.type is CityVisionMapUpdated:
            self._city_visible_cells = packet.args
        elif packet.type is NextTurn:
            self._units_visible_cells = set()
            self._city_visible_cells = set()

    def render_cell(self,
                    surface: pygame.Surface,
                    cell_size: int,
                    row: int,
                    column: int,
                    camera: Camera,
                    cell_rect: pygame.Rect):
        if (row, column) not in self._units_visible_cells | self._city_visible_cells:
            fog_texture = pygame.transform.scale(self._FOG_TEXTURE, (cell_size - 2, cell_size - 2))
            surface.blit(fog_texture, (cell_rect[0] + 1, cell_rect[1] + 1))
