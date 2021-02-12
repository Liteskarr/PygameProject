from typing import Tuple

import pygame
import pygame_gui
from pygame_gui.ui_manager import UIManager
from pygame_gui.elements import UIButton, UITextEntryLine, UITextBox, UILabel, UIDropDownMenu

from pygame_engine.window import Window

from src.camera import Camera
from src.game_component import GameComponent
from src.data_packet import DataPacket
from src.data_packets.all import (ConsoleCommand,
                                  ConsoleMessage,
                                  NeedsGameClosing,
                                  NeedsGameSaving,
                                  UnitChosen,
                                  UnitLeft,
                                  NeedsNextTurn,
                                  NextPlayer,
                                  CityChosen,
                                  CityLeft,
                                  ClickedAtCell,
                                  UnitCouldSpawned,
                                  PlayerUpdated)
from src.player import Player
from src.units_building import COST_BY_TYPE, NAME_BY_TYPE


class GUIComponent(GameComponent):
    def init(self):
        self._current_player: Player = None
        self._current_cell: Tuple[int, int] = None
        self.ui_manager = UIManager(Window.get_size())
        self._width, self._height = Window.get_size()
        self.init_ui()

    def init_ui(self):
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.exit_button = UIButton(
            manager=self.ui_manager,
            text='Меню',
            relative_rect=pygame.Rect((self._width - 100, 0), (100, 50))
        )
        self.exit_button.font = font
        self.exit_button.rebuild()

        self.save_button = UIButton(
            manager=self.ui_manager,
            text='Сохранить',
            relative_rect=pygame.Rect((self._width - 100, 50), (100, 50))
        )
        self.save_button.font = font
        self.save_button.rebuild()

        self.command_line = UITextEntryLine(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((0, 200), (400, 25))
        )
        self.command_line.hide()

        self.console_log = UITextBox(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((0, 0), (400, 200)),
            html_text=''
        )
        self.console_log.hide()

        self.fps_text = UILabel(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((self._width - 150, 0), (50, 50)),
            text=''
        )
        self.fps_text.font = font
        self.fps_text.rebuild()

        self.next_turn_button = UIButton(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((self._width - 200, self._height - 100), (200, 100)),
            text='Следующий ход...',
        )
        self.next_turn_button.font = font
        self.next_turn_button.rebuild()

        self.unit_info_text = UITextBox(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((0, self._height - 200), (400, 200)),
            html_text=''
        )
        self.unit_info_text.font = font
        self.unit_info_text.rebuild()
        self.unit_info_text.hide()

        self.town_info_text = UITextBox(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((0, self._height - 400), (400, 400)),
            html_text=''
        )
        self.town_info_text.font = font
        self.town_info_text.rebuild()
        self.town_info_text.hide()

        self.units_list = UIDropDownMenu(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((0, self._height - 425), (400, 25)),
            starting_option=list(NAME_BY_TYPE.keys())[0],
            options_list=list(NAME_BY_TYPE.keys())
        )
        self.units_list.font = font
        self.units_list.rebuild()
        self.units_list.hide()

        self.build_button = UIButton(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((0, self._height - 450), (400, 25)),
            text='Построить'
        )
        self.build_button.font = font
        self.build_button.rebuild()
        self.build_button.hide()

        self.head_label = UILabel(
            manager=self.ui_manager,
            relative_rect=pygame.Rect((200, 0), (900, 50)),
            text=''
        )
        self.head_label.font = font
        self.head_label.rebuild()

    def handle_packet(self, packet: DataPacket):
        if packet.type is ConsoleMessage:
            self.print_at_console(packet.args)
        elif packet.type is UnitChosen:
            self.handle_unit_choosing(packet)
        elif packet.type is UnitLeft:
            self.handle_unit_leaving()
        elif packet.type is NextPlayer:
            self.handle_next_player(packet)
        elif packet.type is CityChosen:
            self.handle_city_choosing(packet)
        elif packet.type is CityLeft:
            self.handle_city_left(packet)
        elif packet.type is ClickedAtCell:
            self.handle_clicking_at_cell(packet)
        elif packet.type is PlayerUpdated:
            self.handle_next_player(packet)

    def handle_clicking_at_cell(self, packet: DataPacket):
        self._current_cell = packet.args

    def handle_city_choosing(self, packet: DataPacket):
        self.town_info_text.show()
        self.build_button.show()
        self.units_list.show()

    def handle_city_left(self, packet: DataPacket):
        self.town_info_text.hide()
        self.build_button.hide()
        self.units_list.hide()

    def handle_next_player(self, packet: DataPacket):
        self._current_player = packet.args.player
        turn, player = packet.args
        self.head_label.text = f'Ход: {turn}{" " * 3}Игрок: {player.name}{" " * 3}'
        self.handle_resources_updating(player)
        self.head_label.rebuild()

    def handle_resources_updating(self, player: Player):
        resources, manpower = player.resources, player.manpower
        self.head_label.text += f'Ресурсы: {resources}{" " * 3}Людские ресурсы: {manpower}'
        self.head_label.rebuild()

    def handle_unit_choosing(self, packet: DataPacket):
        row, column, pos, unit = packet.args
        self.unit_info_text.html_text += f'<font face=Montserrat color=regular_text><font size=7>'
        self.unit_info_text.html_text += f'Владелец: {unit.get_owner().name}<br>'
        self.unit_info_text.html_text += f'Расположение: {row + 1},{column + 1}<br>'
        self.unit_info_text.html_text += f'Очки передвижения: {unit.get_moving_points()}<br>'
        self.unit_info_text.html_text += f'Текущий POW: {unit.count_pow()}<br>'
        self.unit_info_text.html_text += f'Стандартный POW: {unit.get_default_pow()}'
        self.unit_info_text.html_text += f'</font></font>'
        self.unit_info_text.rebuild()
        self.unit_info_text.show()

    def handle_unit_leaving(self):
        self.unit_info_text.html_text = ''
        self.unit_info_text.rebuild()
        self.unit_info_text.hide()

    def try_build_unit(self):
        unit_type = NAME_BY_TYPE[self.units_list.selected_option]
        owner = self._current_player
        row, column = self._current_cell
        self.push_packet(DataPacket.fast_message_construct(UnitCouldSpawned, row, column, unit_type, owner))

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
                    self.push_packet(DataPacket.fast_message_construct(NeedsGameClosing))
                elif event.ui_element == self.save_button:
                    self.push_packet(DataPacket.fast_message_construct(NeedsGameSaving))
                elif event.ui_element == self.next_turn_button:
                    self.push_packet(DataPacket.fast_message_construct(NeedsNextTurn))
                elif event.ui_element == self.build_button:
                    self.try_build_unit()

    def update(self, delta_time: float):
        self.fps_text.set_text(str(int(1 / delta_time)))
        self.ui_manager.update(delta_time)

    def render_at_screen(self,
                         screen: pygame.Surface,
                         camera: Camera):
        self.ui_manager.draw_ui(screen)
