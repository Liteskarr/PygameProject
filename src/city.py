from src.player import Player


class City:
    _VISION_RADIUS = 3

    def __init__(self,
                 name: str,
                 owner: Player,
                 manpower_adding: int,
                 resources_adding: int):
        self._name = name
        self._owner = owner
        self._manpower_adding = manpower_adding
        self._resources_adding = resources_adding

    def get_name(self) -> str:
        return self._name

    def set_owner(self, owner: Player):
        self._owner = owner

    def get_owner(self) -> Player:
        return self._owner

    def get_manpower_adding(self) -> int:
        return self._manpower_adding

    def get_resources_adding(self) -> int:
        return self._resources_adding

    def next_turn(self):
        self._owner.manpower += self.get_manpower_adding()
        self._owner.resources += self.get_resources_adding()

    def get_vision_radius(self):
        return self._VISION_RADIUS
