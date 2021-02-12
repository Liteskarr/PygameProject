import os
import pickle
from typing import Dict, Tuple
import pathlib

import pygame

from src.data_packet import DataPacket
from src.game_component import GameComponent
from src.city import City
from src.data_packets.all import (NextTurn,
                                  ClickedAtCity,
                                  CityChosen,
                                  CityLeft,
                                  NextPlayer,
                                  CityVisionMapUpdated,
                                  Camera,
                                  ClickedAtAbyss,
                                  ClickedAtCell,
                                  PlayerUpdated,
                                  UnitMoved)
from src.player import Player


class CitiesComponent(GameComponent):
    _TEXTURE: pygame.Surface = None

    def __init__(self):
        self._cities: Dict[Tuple[int, int], City] = {}
        self._current_player: Player = None

    def handle_packet(self, packet: DataPacket):
        if packet.type is ClickedAtCity:
            self.handle_clicking_at_city(packet)
        elif packet.type is ClickedAtCell:
            self.handle_city_left(packet)
        elif packet.type is CityChosen:
            self.handle_city_choosing(packet)
        elif packet.type is NextPlayer:
            self.handle_next_player(packet)
        elif packet.type is NextTurn:
            self.handle_next_turn(packet)
        elif packet.type is UnitMoved:
            self.handle_unit_moving(packet)

    def handle_unit_moving(self, packet: DataPacket):
        trow, tcolumn, unit = packet.args.trow, packet.args.tcolumn, packet.args.unit
        if (trow, tcolumn) in self._cities:
            self._cities[trow, tcolumn].set_owner(unit.get_owner())
            self.push_packet(DataPacket.fast_message_construct(CityVisionMapUpdated))

    def handle_clicking_at_city(self, packet: DataPacket):
        row, column = packet.args
        if (row, column) not in self._cities:
            self.handle_city_left(packet)
        else:
            self.push_packet(DataPacket.fast_message_construct(CityChosen, row, column, self._cities[row, column]))

    def handle_city_choosing(self, packet: DataPacket):
        pass

    def handle_city_left(self, packet: DataPacket):
        self.push_packet(DataPacket.fast_message_construct(CityLeft))

    def handle_next_turn(self, packet: DataPacket):
        for city in self._cities.values():
            city.next_turn()
            self.push_packet(DataPacket.fast_message_construct(
                PlayerUpdated, packet.args.turn, city.get_owner()
            ))

    def handle_next_player(self, packet: DataPacket):
        self._current_player = packet.args.player
        self.update_vision_map()

    def update_vision_map(self):
        result: set = set()
        for cell, city in self._cities.items():
            row, column = cell
            if not self._current_player.could_see_as(city.get_owner()):
                continue
            for dr in range(-city.get_vision_radius() + 1, city.get_vision_radius()):
                for dc in range(-city.get_vision_radius() + 1, city.get_vision_radius()):
                    result.add((row + dr, column + dc))
        self.push_packet(DataPacket.fast_message_construct(CityVisionMapUpdated, result))

    def add_city(self, row: int, column: int, city: City):
        self._cities[row, column] = city

    def render_cell(self,
                    surface: pygame.Surface,
                    cell_size: int,
                    row: int,
                    column: int,
                    camera: Camera,
                    cell_rect: pygame.Rect):
        if (row, column) in self._cities:
            if self._TEXTURE is None:
                self._TEXTURE = pygame.image.load('../data/textures/city.png')
            player = self._cities[row, column].get_owner()
            minor_color = player.minor_color
            major_color = player.major_color
            city_icon = pygame.transform.scale(self._TEXTURE, (cell_size // 2, cell_size // 2))
            pygame.draw.ellipse(surface, major_color, [cell_rect[0], cell_rect[1] + cell_size // 2,
                                                       cell_size // 2, cell_size // 2])
            pygame.draw.ellipse(surface, minor_color, [cell_rect[0], cell_rect[1] + cell_size // 2,
                                                       cell_size // 2, cell_size // 2], 3)
            surface.blit(city_icon, (cell_rect[0], cell_rect[1] + cell_size // 2))

    def load(self, saving: str):
        cities = f'{saving}/cities'
        pathlib.Path(cities).mkdir(parents=True, exist_ok=True)
        for file in os.listdir(cities):
            row, column = map(int, file.split('_'))
            city = pickle.load(open(f'{cities}/{file}', 'rb+'))
            self._cities[row, column] = city

    def save(self, saving: str):
        cities = f'{saving}/cities'
        pathlib.Path(cities).mkdir(parents=True, exist_ok=True)
        for cell, city in self._cities.items():
            pickle.dump(city, open(f'{cities}/{cell[0]}_{cell[1]}', 'wb+'))
