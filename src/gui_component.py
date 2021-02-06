import pygame
import pygame_gui
from pygame_gui.ui_manager import UIManager
from pygame_gui.elements import UIButton, UITextEntryLine, UITextBox, UILabel

from pygame_engine.window import Window

from src.camera import Camera
from src.game_component import GameComponent
from src.data_packet import DataPacket
from src.data_packet_types.all import (ConsoleCommand,
                                       ConsoleMessage,
                                       NeedsGameClosing,
                                       NeedsGameSaving,
                                       UnitChosen,
                                       UnitMoved,
                                       UnitLeft, NeedsNextTurn, NextPlayer)
from src.player import Player


class GUIComponent(GameComponent):
    def init(self):
        self.ui_manager = UIManager(Window.get_size())
        self._width, self._height = Window.get_size()
        self.init_ui()

    def init_ui(self):
        self.exit_button = UIButton(
            manager=self.ui_manager,
            text='Выйти',
            relative_rect=pygame.Rect((self._width - 100, 0), (100, 50)),
        )

        self.save_button = UIButton(
            manager=self.ui_manager,
            text='Сохранить',
            relative_rect=pygame.Rect((self._width - 100, 50), (100, 50))
        )

        self.command_line = UITextEntryLine(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((0, 200), (400, 25))
        )

        self.console_log = UITextBox(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((0, 0), (400, 200)),
            html_text=''
        )

        self.fps_text = UILabel(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((self._width - 150, 0), (50, 50)),
            text=''
        )

        self.next_turn_button = UIButton(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((self._width - 200, self._height - 100), (200, 100)),
            text='Следующий ход...',
        )

        self.unit_info_text = UITextBox(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((0, self._height - 200), (400, 200)),
            html_text=''
        )

        self.head_label = UILabel(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((400, 0), (500, 25)),
            text=''
        )

    def handle_packet(self, packet: DataPacket):
        if packet.type is ConsoleMessage:
            self.print_at_console(packet.args)
        elif packet.type is UnitChosen:
            self.handle_unit_choosing(packet)
        elif packet.type is UnitLeft:
            self.handle_unit_leaving()
        elif packet.type is NextPlayer:
            self.handle_next_player(packet)

    def handle_next_player(self, packet: DataPacket):
        turn, player = packet.args
        self.head_label.text = f'Ход: {turn}{" " * 4}Игрок: {player.name}{" " * 4}'
        self.handle_resources_updating(player)
        self.head_label.rebuild()

    def handle_resources_updating(self, player: Player):
        resources, manpower = player.resources, player.manpower
        self.head_label.text += f'Ресурсы: {resources}{" " * 4}Людские ресурсы: {manpower}'
        self.head_label.rebuild()

    def handle_unit_choosing(self, packet: DataPacket):
        row, column, pos, unit = packet.args
        self.unit_info_text.html_text += f'Владелец: {unit.get_owner().name}<br>'
        self.unit_info_text.html_text += f'Расположение: {row + 1},{column + 1}<br>'
        self.unit_info_text.html_text += f'Очки передвижения: {unit.get_moving_points()}<br>'
        self.unit_info_text.html_text += f'Текущий POW: {unit.count_pow()}<br>'
        self.unit_info_text.html_text += f'Стандартный POW: {unit.get_default_pow()}'
        self.unit_info_text.rebuild()

    def handle_unit_leaving(self):
        self.unit_info_text.html_text = ''
        self.unit_info_text.rebuild()

    def print_at_console(self, line: str):
        self.console_log.html_text = f'{self.console_log.html_text}{line}<br>'
        self.console_log.rebuild()

    def handle_event(self, event: pygame.event.Event):
        self.ui_manager.process_events(event)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == self.command_line:
                    self.push_packet(DataPacket(sender=self,
                                                type=ConsoleCommand,
                                                args=ConsoleCommand.args_type(event.text)))
                    self.command_line.text = ''
            elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.exit_button:
                    self.push_packet(DataPacket(
                        sender=self,
                        type=NeedsGameClosing,
                        args=NeedsGameClosing.args_type(exit_code=0,
                                                        message='OK')
                    ))
                elif event.ui_element == self.save_button:
                    self.push_packet(DataPacket(
                        sender=self,
                        type=NeedsGameSaving,
                        args=NeedsGameSaving.args_type()
                    ))
                elif event.ui_element == self.next_turn_button:
                    self.push_packet(
                        DataPacket.fast_message_construct(NeedsNextTurn)
                    )

    def update(self, delta_time: float):
        self.fps_text.set_text(str(int(1 / delta_time)))
        self.ui_manager.update(delta_time)

    def render_at_screen(self,
                         screen: pygame.Surface,
                         camera: Camera):
        self.ui_manager.draw_ui(screen)
