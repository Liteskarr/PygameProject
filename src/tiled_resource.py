# TODO: docs

from typing import Union

from src.resource import Resource, NoneResource


class TiledResource:
    def __init__(self, resource: Union[Resource, type], adding: int):
        self._resource = resource
        self._adding = adding

    def get_resource(self) -> Resource:
        return self._resource

    def get_adding(self) -> int:
        return self._adding


class NoneTiledResource(TiledResource):
    def __init__(self):
        super().__init__(NoneResource, 0)

