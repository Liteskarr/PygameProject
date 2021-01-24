from typing import List
from itertools import cycle

from src.player import Player
from src.world_map import WorldMap


class Game:
    """

    """

    def load_from_file(self):
        pass

    def save_to_file(self):
        pass

    def update(self):
        pass

    def next_turn(self):
        pass

    def get_map(self) -> WorldMap:
        return WorldMap(10, 10)
