from typing import Any, Callable
from dataclasses import dataclass


@dataclass
class DataPacket:
    type: type
    args: Any
    response_function: Callable = lambda: None
    sender: Any = None

    @staticmethod
    def fast_message_construct(packet_type: "DataPacketType", *args, **kwargs) -> "DataPacket":
        packet = DataPacket(type=packet_type,
                            args=packet_type.args_type(*args, **kwargs))
        return packet

    @staticmethod
    def fast_request_construct(packet_type: "DataPacketType", response_function: Callable, *args, **kwargs):
        packet = DataPacket.fast_message_construct(packet_type, *args, **kwargs)
        packet.response_function = response_function
        return packet
