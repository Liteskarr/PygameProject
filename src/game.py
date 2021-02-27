"""
Описание логики игрового процесса.
"""

import os
import json
import pathlib
import pickle
from typing import List, Tuple

import pygame

from src.pygame_engine.engine import Engine

from src.camera import Camera
from src.data_packet import DataPacket
from src.data_packets.all import (NeedsGameSaving,
                                  NeedsGameClosing,
                                  NextTurn,
                                  NextPlayer, NeedsNextTurn, CameraUpdated, ShapeUpdated, CellSizeUpdated,
                                  PlayerUpdated)
from src.game_component import GameComponent
from src.player import Player


class Game:
    """
    Класс, объединяющий все классы взаимодействия с игровым процессом.
    """

    def __init__(self):
        self._init_system()
        self._name: str
        self._sys_name: str
        self._width: int
        self._height: int
        self._camera: Camera
        self._cell_size: int
        self._current_player: int
        self._current_turn: int
        self._players: List

    def _init_system(self):
        """
        Инициализирует системные переменные.
        """
        self.main_menu_scene_cls: type = None
        self._components: List = []

    def init(self,
             name: str,
             sys_name: str,
             width: int,
             height: int,
             camera: Camera = None,
             cell_size: int = 40,
             players: List[Player] = None,
             main_menu_scene_cls: type = None):
        """
        Инициализирует игру на основе пользовательских переменных.
        """
        self._main_menu_scene_cls = main_menu_scene_cls
        self.set_name(name)
        self.set_sys_name(sys_name)
        self.set_cell_size(cell_size)
        if camera is not None:
            self.set_camera(camera)
        self.set_shape(width, height)
        self.set_players_list(players)
        self.restart()

    def load(self, saving: str):
        """
        Загружает игру из файловой системы.
        :param saving: Имя сохранения.
        """
        saving = f'../savings/{saving}'
        base = f'{saving}/base'
        data = json.load(open(f'{base}/base.json', 'r'))
        self.set_name(data['name'])
        self.set_sys_name(data['sys_name'])
        self.set_cell_size(data['cell_size'])
        self.set_shape(data['width'], data['height'])
        self._set_current_turn(data['current_turn'])
        self.set_current_player_index(data['current_player_index'] - 1)
        players = [pickle.load(open(f'{base}/{file}', mode='rb')) for file in os.listdir(base)
                   if file.startswith('p')]
        self.set_players_list(players)
        for components in self.get_all_components():
            components.load(saving)
        self.next_player()

    def save(self, saving: str, prefix: str = '../'):
        """
        Сохраняет игру в файловую систему.
        :param prefix: Префикс пути.
        :param saving: Имя сохранения.
        """
        saving = f'{prefix}savings/{saving}'
        base = f'{saving}/base'
        pathlib.Path(saving).mkdir(parents=True, exist_ok=True)
        pathlib.Path(base).mkdir(parents=True, exist_ok=True)
        json.dump(
            {
                'name': self.get_name(),
                'sys_name': self.get_sys_name(),
                'width': self.get_width(),
                'height': self.get_height(),
                'cell_size': self.get_cell_size(),
                'current_turn': self.get_current_turn(),
                'current_player_index': self.get_current_player_index()
            },
            open(f'{base}/base.json', 'w+', encoding='utf-8')
        )
        for index, player in enumerate(self._players):
            pickle.dump(player, open(f'{base}/p{index}_{player.name}', 'wb+'))
        for component in self.get_all_components():
            component.save(saving)

    def push_packet(self, packet: DataPacket):
        """
        Оповещает все компоненты о новом пакете.
        """
        for component in self._components:
            component.handle_packet(packet)
        self.handle_packet(packet)

    def handle_packet(self, packet: DataPacket):
        if packet.type is NeedsGameClosing:
            if self.main_menu_scene_cls is None:
                Engine.running = False
            else:
                Engine.set_scene(self.main_menu_scene_cls())
        elif packet.type is NeedsGameSaving:
            self.save(self.get_sys_name())
        elif packet.type is NeedsNextTurn:
            self.next_player()
        elif packet.type is PlayerUpdated:
            self._handle_player_updating(packet)

    def _handle_player_updating(self, packet: DataPacket):
        index = self._players.index(packet.args.player)
        self.get_players_list()[index] = packet.args.player

    def restart(self):
        """
        Перезапускает игру.
        :return:
        """
        self._current_player = -1
        self._current_turn = 1
        self.next_player()

    def set_sys_name(self, sys_name: str):
        self._sys_name = sys_name

    def get_sys_name(self) -> str:
        return self._sys_name

    def set_name(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    def set_players_list(self, players: List[Player]):
        self._players = [] if players is None else players

    def get_players_list(self) -> List[Player]:
        return self._players

    def set_cell_size(self, cell_size: int):
        self._cell_size = cell_size
        self.push_packet(
            DataPacket.fast_message_construct(
                CellSizeUpdated,
                self._cell_size
            )
        )

    def get_cell_size(self) -> int:
        return self._cell_size

    def set_camera(self, camera: Camera):
        self._camera = camera
        self.push_packet(
            DataPacket.fast_message_construct(
                CameraUpdated,
                self._camera
            )
        )

    def get_camera(self) -> Camera:
        return self._camera

    def set_shape(self, width: int, height: int):
        self._width = width
        self._height = height
        self.push_packet(
            DataPacket.fast_message_construct(
                ShapeUpdated,
                self.get_width(),
                self.get_height()
            )
        )

    def get_shape(self) -> Tuple[int, int]:
        """
        Возвращает количество клеток по ширине и высоте.
        """
        return self._width, self._height

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def next_player(self):
        """
        Определяет игровое поведение при смене хода.
        """
        self._current_turn += 1
        self._current_player = (self._current_player + 1) % len(self.get_players_list())
        if self._current_turn % len(self.get_players_list()) == 0:
            self.push_packet(
                DataPacket.fast_message_construct(
                    NextTurn,
                    self.get_current_turn())
            )

        self.push_packet(
            DataPacket.fast_message_construct(
                NextPlayer,
                self.get_current_turn(),
                self.get_current_player())
        )

    def _set_current_turn(self, current_turn: int):
        self._current_turn = current_turn

    def get_current_turn(self) -> int:
        """
        Возвращает номер текущего хода.
        """
        return self._current_turn // len(self.get_players_list())

    def set_current_player_index(self, index: int):
        self._current_player = index

    def get_current_player_index(self) -> int:
        return self._current_player

    def get_current_player(self) -> Player:
        return self.get_players_list()[self.get_current_player_index()]

    def update(self, delta_time: float):
        """
        Обновляет компоненты от времени, которое прошло с предыдущего кадра.
        :param delta_time: Вещественное число, обозначающее время в секундах.
        """
        for component in self.get_all_components():
            component.update(delta_time)

    def handle_event(self, event: pygame.event.Event):
        """
        Обрабатывает ивент pygame.
        """
        for component in self.get_all_components():
            component.handle_event(event)

    def init_component(self, component: GameComponent):
        """
        Инициализирует игровой компонент.
        Если компонент с данным типом уже существует, то бросает исключение.
        """
        if type(component) in map(type, self.get_all_components()):
            raise KeyError('Component initialized before!')
        component.set_game(self)
        component.init()
        self._components.append(component)

    def get_component(self, component_type: type) -> GameComponent:
        """
        Возвращает компонент по его типу.
        Если компонент не найден, то кидает исключение.
        """
        for component in self._components:
            if type(component) == component_type:
                return component
        raise IndexError('Component does not initialized!')

    def get_all_components(self) -> List[GameComponent]:
        """
        Возвращает список всех компонентов игры.
        """
        return self._components

    def render_all(self, surface: pygame.Surface):
        """
        Вызывает методы отрисовки компонентов.
        :param surface: Поверхность, на которую будет происходить рисование.
        """
        cx, cy, cw, ch = self._camera.get_rect()
        from_row = max(cy // self._cell_size, 0)
        from_column = max(cx // self._cell_size, 0)
        cell_size = self._cell_size
        for r in range(from_row, self._height):
            dirty_flag = True
            for c in range(from_column, self._width):
                cell_rect = (c * cell_size - cx, r * cell_size - cy, cell_size, cell_size)
                raw_cell_rect = (cell_rect[0] + cx, cell_rect[1] + cy) + cell_rect[2:]
                if self._camera.intersect_with_rect(raw_cell_rect):
                    dirty_flag = False
                    for component in self._components:
                        component.render_cell(surface, int(cell_size), r, c, self._camera, cell_rect)
                else:
                    break
            if dirty_flag:
                break
        for component in self.get_all_components():
            component.render_at_screen(surface, self._camera)
