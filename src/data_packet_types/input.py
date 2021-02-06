from typing import Type
from collections import namedtuple

from src.data_packet_type import DataPacketType


class ClickedAtCell(DataPacketType):
    args_type: Type = namedtuple('Cell', ['row', 'column'])


class ClickedAtUnit(DataPacketType):
    args_type: Type = namedtuple('Unit', ['row', 'column', 'pos'])


class ClickedAtAbyss(DataPacketType):
    pass


class SelectionsCanceled(DataPacketType):
    pass
