# TODO: docs

from src.resource import Resource


class TiledResource:
    def __init__(self, resource: Resource, adding: int):
        self._resource = resource
        self._adding = adding

    def get_resource(self) -> Resource:
        return self._resource

    def get_adding(self) -> int:
        return self._adding
