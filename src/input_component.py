from typing import Tuple

import pygame

from src.camera import Camera
from src.data_packet import DataPacket
from src.data_packets.all import (ClickedAtCell,
                                  ClickedAtUnit,
                                  ClickedAtAbyss,
                                  RequestCellSizeLimit,
                                  CameraUpdated,
                                  SelectionsCanceled,
                                  ShapeUpdated,
                                  CellSizeUpdated,
                                  ClickedAtCity)
from src.game_component import GameComponent


class InputComponent(GameComponent):
    def __init__(self):
        self._camera: Camera
        self._width: int
        self._height: int
        self._cell_size: int
        self._cell_size_limit = 0

    def handle_packet(self, packet: DataPacket):
        if packet.type is CameraUpdated:
            self.handle_camera_updating(packet)
        elif packet.type is ShapeUpdated:
            self.handle_shape_updating(packet)
        elif packet.type is CellSizeUpdated:
            self.handle_cell_size_updating(packet)

    def handle_camera_updating(self, packet: DataPacket):
        self._camera = packet.args.camera

    def handle_cell_size_updating(self, packet: DataPacket):
        self._cell_size = packet.args

    def handle_shape_updating(self, packet: DataPacket):
        self._width, self._height = packet.args

    def process_cell_size_limit_getting_response(self, value: int):
        self._cell_size_limit = value

    def validate_cell(self, row: int, column: int) -> bool:
        return 0 <= row < self._height and 0 <= column < self._width

    def get_cell_screen_position(self, row: int, column: int) -> Tuple[int, int]:
        cx, cy, *_ = self._camera.get_rect()
        return column * self._cell_size - cx, row * self._cell_size - cy

    def get_cell_by_mouse(self, mouse_pos: Tuple[int, int]) -> Tuple[int, int]:
        cell_size = self._cell_size
        cx, cy, *_ = self._camera.get_rect()
        mx, my = mouse_pos
        return (my + cy) // cell_size, (mx + cx) // cell_size

    def handle_event(self, event: pygame.event.Event):
        cx, cy, *_ = self._camera.get_rect()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            mx, my = event.pos
            row, column = self.get_cell_by_mouse(event.pos)
            if self.validate_cell(row, column):
                self.push_packet(DataPacket.fast_message_construct(ClickedAtCell, row, column))
                self.push_packet(DataPacket.fast_request_constructor(RequestCellSizeLimit,
                                                                     self.process_cell_size_limit_getting_response,
                                                                     row, column))
                rx, ry = self.get_cell_screen_position(row, column)

                unit_position = self._cell_size_limit * (mx - rx) // self._cell_size
                if unit_position < self._cell_size_limit and (my - ry) <= self._cell_size // 2:
                    self.push_packet(DataPacket.fast_message_construct(ClickedAtUnit, row, column,
                                                                       unit_position))
                if mx - rx <= self._cell_size // 2 <= my - ry <= self._cell_size:
                    self.push_packet(DataPacket.fast_message_construct(ClickedAtCity, row, column))
            else:
                self.push_packet(DataPacket.fast_message_construct(ClickedAtAbyss))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_MIDDLE:
            self.push_packet(DataPacket.fast_message_construct(SelectionsCanceled))
