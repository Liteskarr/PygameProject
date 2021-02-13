import random

import pygame

from src.biomes.all import *
from src.cities_component import CitiesComponent
from src.city import City
from src.game import Game
from src.player import Player
from src.scenarios.scenario import Scenario, ScenarioBuilder
from src.terrains.all import *
from src.tile import Tile
from src.unit import Unit
from src.units.all import *
from src.units_component import UnitsComponent
from src.world_map_component import WorldMapComponent


class BaseScenarioBuilder(ScenarioBuilder):
    def __init__(self):
        self.player1 = Player(name='Первый игрок',
                              major_color=pygame.Color('black'),
                              minor_color=pygame.Color('blue'),
                              manpower=1000,
                              resources=1000)
        self.player2 = Player(name='Второй игрок',
                              major_color=pygame.Color('black'),
                              minor_color=pygame.Color('red'),
                              manpower=1000,
                              resources=1000)

    def build(self, name: str, sys_name: str):
        self._game = Game()
        self._units = UnitsComponent()
        self._world_map = WorldMapComponent()
        self._cities = CitiesComponent()
        self._game.init_component(self._units)
        self._game.init_component(self._world_map)
        self._game.init_component(self._cities)
        self._game.init(
            name,
            sys_name,
            10,
            10,
            players=[self.player1, self.player2]
        )
        self.init_map()
        self.init_units()
        self.init_cities()

    def init_units(self):
        width, height = self._game.get_shape()
        self._units.add_unit(0, 0, Unit(IrregularType, self.player1))
        self._units.add_unit(width - 1, height - 1, Unit(IrregularType, self.player2))

    def init_map(self):
        width, height = self._game.get_shape()
        for row in range(height):
            for column in range(width):
                tile = Tile(TemperateBiome, PlainTerrain if random.random() >= 0.3 else HillTerrain)
                self._world_map.set_tile(row, column, tile)

    def init_cities(self):
        self._cities.add_city(0, 0, City(
            name='Хельмова Падь',
            owner=self.player1,
            manpower_adding=10,
            resources_adding=10
        ))

        self._cities.add_city(9, 9, City(
            name='Гондор',
            owner=self.player2,
            manpower_adding=50,
            resources_adding=50
        ))

    def get_prefix(self) -> str:
        return 'base_scenario_'

    def save(self, saving: str):
        self._game.save(saving, prefix='../')
