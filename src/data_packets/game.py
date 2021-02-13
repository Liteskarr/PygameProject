from typing import Type
from collections import namedtuple

from src.camera import Camera
from src.data_packet_type import DataPacketType


class NeedsGameSaving(DataPacketType):
    pass


class NeedsGameClosing(DataPacketType):
    pass


class NeedsNextTurn(DataPacketType):
    pass


class NeedsAllPlayers(DataPacketType):
    pass


class NextTurn(DataPacketType):
    args_type: Type = namedtuple('Turn', ['turn'])


class NextPlayer(DataPacketType):
    args_type: Type = namedtuple('Turn', ['turn', 'player'])


class CameraUpdated(DataPacketType):
    args_type: Type = namedtuple('Camera', ['camera'])


class ShapeUpdated(DataPacketType):
    args_type: Type = namedtuple('Shape', ['width', 'height'])


class CellSizeUpdated(DataPacketType):
    args_type: Type = int


class PlayerUpdated(DataPacketType):
    args_type: Type = namedtuple('Context', ['turn', 'player'])


class NeedsPlayerChecking(DataPacketType):
    args_type: Type = namedtuple('Turn', ['turn', 'player'])
