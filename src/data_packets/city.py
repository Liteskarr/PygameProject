from typing import Type
from collections import namedtuple

from src.data_packet_type import DataPacketType


class CityChosen(DataPacketType):
    args_type: Type = namedtuple('Cell', ['row', 'column', 'city'])


class CityLeft(DataPacketType):
    pass


class UnitWasSpawned(DataPacketType):
    args_type: Type = namedtuple('UnitCost', ['owner', 'manpower', 'resources'])


class UnitCouldSpawned(DataPacketType):
    args_type: Type = namedtuple('Unit', ['row', 'column', 'type', 'owner'])


class CityVisionMapUpdated(DataPacketType):
    args_type: Type = set
