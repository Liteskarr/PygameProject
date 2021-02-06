from typing import Type, Tuple, Set
from collections import namedtuple

from src.data_packet_type import DataPacketType


class UnitChosen(DataPacketType):
    args_type: Type = namedtuple('Cell', ['row', 'column', 'pos', 'unit'])


class UnitMoved(DataPacketType):
    args_type: Type = namedtuple('Positions', ['frow', 'fcolumn', 'fpos', 'trow', 'tcolumn'])


class UnitLeft(DataPacketType):
    pass


class VisionMapUpdated(DataPacketType):
    args_type: Type = set


class RequestCellSizeLimit(DataPacketType):
    args_type: Type = namedtuple('Cell', ['row', 'column'])
