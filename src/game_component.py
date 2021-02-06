import pygame

from src.camera import Camera
from src.data_packet import DataPacket


class GameComponent:
    def init(self):
        pass

    def set_game(self, game: "Game"):
        """
        Устанавливает ссылку на ко
        :param game:
        """
        self._game = game

    def get_game(self) -> "Game":
        """

        :return:
        """
        return self._game

    def get_component(self, component: type) -> "GameComponent":
        """

        :param component:
        """
        return self._game.get_component(component)

    def push_packet(self, packet: DataPacket):
        """

        :param packet:
        """
        packet.sender = self
        self.get_game().push_packet(packet)

    def handle_packet(self, packet: DataPacket):
        """

        :param packet:
        """
        pass

    def handle_event(self, event: pygame.event.Event):
        """

        :param event:
        """
        pass

    def update(self, delta_time: float):
        """

        :param delta_time:
        """
        pass

    def render_at_screen(self,
                         screen: pygame.Surface,
                         camera: Camera):
        """

        :param screen:
        :param camera:
        """
        pass

    def render_cell(self,
                    surface: pygame.Surface,
                    cell_size: int,
                    row: int,
                    column: int,
                    camera: Camera,
                    cell_rect: pygame.Rect):
        """
        :param surface:
        :param cell_size:
        :param row:
        :param column:
        :param camera:
        :param cell_rect:
        """
        pass

    def load(self, saving: str):
        pass

    def save(self, saving: str):
        pass
