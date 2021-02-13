from src.data_packets.all import (NextPlayer,
                                  NeedsNextTurn,
                                  NeedsPlayerChecking)
from src.data_packet import DataPacket
from src.game_component import GameComponent
from src.player import Player


class JudgeComponent(GameComponent):
    def __init__(self):
        self._losers: set = set()
        self._current_value = False

    def add_loser(self, player: Player):
        self._losers.add(player)

    def handle_packet(self, packet: DataPacket):
        if packet.type is NextPlayer:
            self.handle_next_player(packet)

    def handle_next_player(self, packet: DataPacket):
        if packet.args.player in self._losers:
            self.push_packet(DataPacket.fast_message_construct(NeedsNextTurn))
        else:
            self._current_value = False
            self.push_packet(DataPacket.fast_request_construct(
                NeedsPlayerChecking,
                self.process_player_checking,
                packet.args.turn,
                packet.args.player
            ))
            if not self._current_value:
                self._losers.add(packet.args.player)

    def process_player_checking(self, value: bool):
        self._current_value |= value
