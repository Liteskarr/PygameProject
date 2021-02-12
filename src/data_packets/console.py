from typing import Type
from collections import namedtuple

from src.data_packet_type import DataPacketType


class ConsoleMessage(DataPacketType):
    args_type: Type = str


class ConsoleCommand(DataPacketType):
    args_type: Type = str
