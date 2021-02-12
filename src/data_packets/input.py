from typing import Type, List
from collections import namedtuple

import pygame

from src.data_packet_type import DataPacketType


class ClickedAtCell(DataPacketType):
    args_type: Type = namedtuple('Cell', ['row', 'column'])


class ClickedAtUnit(DataPacketType):
    args_type: Type = namedtuple('Unit', ['row', 'column', 'pos'])


class ClickedAtCity(DataPacketType):
    args_type: Type = namedtuple('Cell', ['row', 'column'])


class ClickedAtAbyss(DataPacketType):
    pass


class SelectionsCanceled(DataPacketType):
    pass
