import os
import pathlib
import pickle
import shutil
from collections import defaultdict, deque
from copy import copy
from math import exp, ceil
from typing import List, Tuple, Dict, Iterator, Union, Set

import pygame

from src.camera import Camera
from src.data_packet import DataPacket
from src.data_packets.all import (ClickedAtCell,
                                  ClickedAtUnit,
                                  ConsoleCommand,
                                  ClickedAtAbyss,
                                  RequestCellSizeLimit,
                                  RequestMovementCost,
                                  UnitChosen,
                                  UnitMoved,
                                  UnitLeft,
                                  UnitVisionMapUpdated,
                                  NextTurn,
                                  NextPlayer,
                                  SelectionsCanceled,
                                  ShapeUpdated,
                                  UnitCouldSpawned,
                                  PlayerUpdated,
                                  NeedsPlayerChecking)
from src.game_component import GameComponent
from src.player import Player
from src.pow_modifier import POWModifierKind, POWModifier, get_final_pow
from src.unit import Unit
from src.units_building import COST_BY_TYPE


def get_damage(unit_pow: int, enemy_pow: int) -> int:
    pow_difference = unit_pow - enemy_pow
    base = enemy_pow
    modifier = exp(0.1 * pow_difference)
    k = 3
    return ceil(base + modifier + k) // k


def update_dict(d: dict, key, value):
    d[key] = value


class UnitsContainer:
    """
    Класс-контейнер для юитов, находящихся на одной клетке.
    """
    def __init__(self, size_limit: int = 2):
        self.size_limit = size_limit
        self._units: List[Unit] = []

    def add(self, unit: Unit):
        if len(self) == self.size_limit:
            raise OverflowError('UnitsContainer is full now!')
        self._units.append(unit)
        self._units.sort(key=lambda u: (u.count_priority(), u.count_pow()), reverse=True)

    def erase(self, index: int):
        self._units.pop(index)

    def get(self, index: int) -> Unit:
        return self._units[index]

    def pop(self, index: int) -> Unit:
        unit = self.get(index)
        self.erase(index)
        return unit

    def iterator(self) -> Iterator[Unit]:
        for unit in self._units:
            yield unit

    def front(self) -> Unit:
        return self._units[0]

    def back(self) -> Unit:
        return self._units[-1]

    def full(self) -> bool:
        return self.size_limit == len(self._units)

    def __len__(self):
        return len(self._units)


class UnitsComponent(GameComponent):
    def __init__(self):
        self._width: int
        self._height: int
        self._player: Player
        self._turn: int
        self._units: Dict[Tuple[int, int], UnitsContainer] = defaultdict(UnitsContainer)
        self._chosen_unit: Union[Tuple[int, int, int], None] = None
        self._moving_cost: Dict[Tuple[int, int], int] = defaultdict(int)
        self._pow_modifiers: List[POWModifier] = []

    def handle_packet(self, packet: DataPacket):
        if packet.type is ClickedAtUnit:
            self.handle_unit_choosing(packet)
        elif packet.type is ClickedAtCell:
            self.handle_cell_choosing(packet)
        elif packet.type is ClickedAtAbyss:
            self.handle_abyss_choosing()
        elif packet.type is RequestCellSizeLimit:
            self.handle_cell_size_limit_request(packet)
        elif packet.type is UnitMoved:
            self.handle_unit_moving()
        elif packet.type is NextTurn:
            self.handle_next_turn(packet)
        elif packet.type is NextPlayer:
            self.handle_next_player(packet)
        elif packet.type is SelectionsCanceled:
            self.handle_abyss_choosing()
        elif packet.type is ShapeUpdated:
            self.handle_shape_updating(packet)
        elif packet.type is UnitCouldSpawned:
            self.try_to_spawn_unit(packet)
        elif packet.type is NeedsPlayerChecking:
            self.handle_player_checking(packet)

    def handle_player_checking(self, packet: DataPacket):
        for container in self._units.values():
            for unit in container.iterator():
                if packet.args.player.could_manage(unit.get_owner()):
                    packet.response_function(True)
                    return
        packet.response_function(False)

    def handle_shape_updating(self, packet: DataPacket):
        self._width, self._height = packet.args

    def handle_unit_choosing(self, packet: DataPacket):
        if (
                self._chosen_unit is None
                and
                packet.args.pos < len(self.get_units_container(packet.args.row, packet.args.column))
        ):
            self._chosen_unit = packet.args
            row, column, pos = packet.args
            self.push_packet(DataPacket.fast_message_construct(UnitChosen, row, column, pos,
                                                               self.get_unit(row, column, pos)))
        else:
            self._chosen_unit = None
            self.push_packet(DataPacket.fast_message_construct(UnitLeft))

    def handle_cell_choosing(self, packet: DataPacket):
        if self._chosen_unit is not None and self._chosen_unit[:2] != packet.args:
            self.make_moving(*self._chosen_unit, *packet.args)
            self.update_vision_map()
            self.push_packet(DataPacket.fast_message_construct(UnitLeft))

    def handle_abyss_choosing(self):
        self._chosen_unit = None
        self.push_packet(DataPacket.fast_message_construct(UnitLeft))

    def handle_cell_size_limit_request(self, packet: DataPacket):
        packet.response_function(self.get_units_container(*packet.args).size_limit)

    def handle_next_turn(self, packet: DataPacket):
        self._turn = packet.args.turn
        for container in self._units.values():
            for unit in container.iterator():
                unit.next_turn(packet.args.turn)

    def handle_next_player(self, packet: DataPacket):
        self._player = packet.args.player
        self.update_vision_map()

    def handle_unit_moving(self):
        self.push_packet(DataPacket.fast_message_construct(UnitLeft))

    def process_cell_pow_modifiers_getting_response(self, modifiers: List[POWModifier]):
        self._pow_modifiers += modifiers

    def process_cell_movement_cost_getting_response(self, row: int, column: int, value: int):
        self._moving_cost[row, column] = value

    def try_to_spawn_unit(self, packet: DataPacket):
        row, column, unit_type, owner = packet.args
        manpower, resources = COST_BY_TYPE[unit_type]
        if (
                owner.manpower >= manpower
                and
                owner.resources >= resources
                and
                not self.get_units_container(row, column).full()
        ):
            owner.manpower -= manpower
            owner.resources -= resources
            self.add_unit(row, column, Unit(unit_type, owner))
            self.push_packet(DataPacket.fast_message_construct(PlayerUpdated, self._turn, owner))

    def get_unit(self, row: int, column: int, pos: int):
        return self._units[row, column].get(pos)

    def get_units_container(self, row: int, column: int) -> UnitsContainer:
        return self._units[row, column]

    def add_unit(self, row: int, column: int, unit: Unit):
        self._units[row, column].add(copy(unit))
        self.update_vision_map()

    def move_unit(self, frow: int, fcolumn: int, fpos: int, trow: int, tcolumn: int):
        unit = self._units[frow, fcolumn].pop(fpos)
        self._units[trow, tcolumn].add(unit)
        self.push_packet(DataPacket.fast_message_construct(UnitMoved, frow, fcolumn, fpos, trow, tcolumn, unit))

    def pop_unit(self, row: int, column: int, pos: int):
        return self.get_units_container(row, column).pop(pos)

    def update_vision_map(self):
        distance: Dict[Tuple[int, int], int] = {}
        queue = deque()
        for row, column in self._units.keys():
            container = self.get_units_container(row, column)
            for unit in container.iterator():
                if self._player.could_see_as(unit.get_owner()):
                    queue.append((row, column))
                    distance[row, column] = max(distance.get((row, column), 0), unit.get_vision_radius())
        while len(queue):
            row, column = queue.popleft()
            if distance[row, column] == 0:
                continue
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    if not (dr == dc == 0):
                        drow, dcolumn = row + dr, column + dc
                        if 0 <= drow < self._height and 0 <= dcolumn < self._width:
                            if (drow, dcolumn) not in distance:
                                distance[drow, dcolumn] = distance[row, column] - 1
                                queue.append((drow, dcolumn))
            result = set([cell for cell in distance.keys()])
            self.push_packet(DataPacket.fast_message_construct(UnitVisionMapUpdated, result))

    def get_distances_from(self, row: int, column: int, owner: Player) -> Dict[Tuple[int, int], int]:
        self.push_packet(DataPacket.fast_request_construct(RequestMovementCost,
                                                           self.process_cell_movement_cost_getting_response))
        local_inf = 2 ** 64
        distance: Dict[Tuple[int, int], int] = {(row, column): 0}
        used: Set[Tuple[int, int]] = set()
        while True:
            vertex = row, column
            for r, c in distance.keys():
                if (r, c) not in used and distance[vertex] < distance[r, c]:
                    vertex = r, c
            used.add(vertex)

            if len(distance) > 1 and vertex == (row, column):
                break

            container = self.get_units_container(*vertex)
            if len(container) and container.front().get_owner() != owner:
                continue

            for drow in range(-1, 2):
                for dcolumn in range(-1, 2):
                    nrow, ncolumn = vertex[0] + drow, vertex[1] + dcolumn
                    if drow == dcolumn == 0:
                        continue
                    if 0 <= nrow < self._height and 0 <= ncolumn < self._width:
                        distance.update({(nrow, ncolumn):
                                             min(distance[vertex] + self._moving_cost[nrow, ncolumn],
                                                 distance.get((nrow, ncolumn), local_inf))})
        return distance

    def get_distance_between(self,
                             frow: int,
                             fcolumn: int,
                             trow: int,
                             tcolumn: int,
                             player: Player) -> Tuple[bool, int]:
        distances = self.get_distances_from(frow, fcolumn, player)
        return (trow, tcolumn) in distances.keys(), distances.get((trow, tcolumn), -1)

    def make_moving(self, frow: int, fcolumn: int, fpos: int, trow: int, tcolumn: int):
        fcontainer = self.get_units_container(frow, fcolumn)
        tcontainer = self.get_units_container(trow, tcolumn)
        if len(fcontainer) <= fpos:
            return
        funit = fcontainer.get(fpos)
        if not self._player.could_manage(funit.get_owner()):
            return
        path_exist, distance = self.get_distance_between(frow, fcolumn, trow, tcolumn, funit.get_owner())
        if not path_exist or funit.get_moving_points() < distance:
            return
        if len(tcontainer) and tcontainer.front().get_owner() != funit.get_owner():
            tunit = tcontainer.front()
            flag_of_die = False
            if not tunit.is_peaceful():
                fpow = get_final_pow(funit.get_default_pow(), funit.get_all_modifiers())
                tpow = get_final_pow(tunit.get_default_pow(), tunit.get_all_modifiers())
                fdamage = get_damage(fpow, tpow)
                tdamage = get_damage(tpow, fpow)
                if funit.use_range_attack():
                    tunit.set_damage(tdamage, self._turn)
                    tunit.apply_modifier(POWModifier(False,
                                                     1,
                                                     self.get_game().get_current_turn(),
                                                     tdamage // 4,
                                                     POWModifierKind.DISORGANIZATION))
                    funit.after_attack()
                elif abs(frow - trow) + abs(fcolumn - tcolumn) <= 2:
                    funit.set_damage(fdamage, self._turn)
                    tunit.set_damage(tdamage, self._turn)
                    if tunit.use_range_attack():
                        tunit.set_damage(tdamage, self._turn)
                    funit.after_attack()
                if not funit.is_alive():
                    self.pop_unit(frow, fcolumn, fpos)
                    flag_of_die = True
                if not tunit.is_alive():
                    self.pop_unit(trow, tcolumn, 0)
            while len(tcontainer) and (tunit := tcontainer.front()) and tunit.is_peaceful():
                tcontainer.pop(0)
            if not len(tcontainer) and not flag_of_die:
                self.move_unit(frow, fcolumn, fpos, trow, tcolumn)
        else:
            if len(tcontainer) < tcontainer.size_limit:
                self.move_unit(frow, fcolumn, fpos, trow, tcolumn)
                funit.decrease_moving_points(distance)
        self.update_vision_map()

    def get_unit_render(self,
                        unit_size: int,
                        row: int,
                        column: int,
                        pos: int) -> pygame.Surface:
        surface = pygame.Surface((unit_size, unit_size))
        surface = pygame.Surface.convert_alpha(surface)
        surface.fill((0, 0, 0, 0))
        unit = self.get_unit(row, column, pos)
        unit_icon = unit.get_resource().get_icon()
        unit_icon = pygame.transform.scale(unit_icon, (unit_size, unit_size))
        major_color = unit.get_owner().major_color
        minor_color = unit.get_owner().minor_color
        pygame.draw.ellipse(surface, major_color, [0, 0, unit_size - 2, unit_size - 2])
        pygame.draw.ellipse(surface, minor_color, [0, 0, unit_size - 2, unit_size - 2], 3)
        font = pygame.font.Font(pygame.font.get_default_font(), 256)
        k = 2.75
        pow_surface = font.render(f'{unit.count_pow():02d}', True, pygame.Color('white'), pygame.Color('black'))
        pow_surface = pygame.transform.scale(pow_surface, (int(unit_size / k), int(unit_size / k)))
        unit_icon.blit(pow_surface, (int((k - 1) * unit_size / k), int((k - 1) * unit_size / k)))
        moving_surface = font.render(f'{unit.get_moving_points():02d}', True, pygame.Color('white'),
                                     pygame.Color('black'))
        moving_surface = pygame.transform.scale(moving_surface, (int(unit_size / k), int(unit_size / k)))
        unit_icon.blit(moving_surface, (0, int((k - 1) * unit_size / k)))
        surface.blit(unit_icon, (0, 0))
        return surface

    def render_cell(self,
                    surface: pygame.Surface,
                    cell_size: int,
                    row: int,
                    column: int,
                    camera: Camera,
                    cell_rect: pygame.Rect):
        unit_size = cell_size // max(2, len(self.get_units_container(row, column)))
        for pos, unit in enumerate(self.get_units_container(row, column).iterator()):
            unit_surface = self.get_unit_render(unit_size, row, column, pos)
            surface.blit(unit_surface, (cell_rect[0] + cell_size // 2 * pos + 1, cell_rect[1] + 1))

    def load(self, saving: str):
        units = f'{saving}/units'
        for file in os.listdir(units):
            row, column = map(int, file.split('_'))
            container = pickle.load(open(f'{units}/{file}', 'rb'))
            self._units[row, column] = container

    def save(self, saving: str):
        units = f'{saving}/units'
        if os.path.exists(units):
            shutil.rmtree(units)
        pathlib.Path(units).mkdir(parents=True, exist_ok=True)
        for cell, container in self._units.items():
            pickle.dump(container, open(f'{units}/{cell[0]}_{cell[1]}', 'wb+'))
