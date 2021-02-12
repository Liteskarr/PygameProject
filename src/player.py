from dataclasses import dataclass

import pygame


@dataclass
class Player:
    minor_color: pygame.Color
    major_color: pygame.Color

    name: str

    resources: int = 0
    manpower: int = 0

    def could_manage(self, obj_owner):
        return self == obj_owner

    def could_see_as(self, obj_owner):
        return self == obj_owner

    def __eq__(self, other: "Player"):
        return self.name == other.name


class God(Player):
    def could_manage(self, obj_owner):
        return True

    def could_see_as(self, obj_owner):
        return True


class Spectator(Player):
    def could_manage(self, obj_owner):
        return False

    def could_see_as(self, obj_owner):
        return True
