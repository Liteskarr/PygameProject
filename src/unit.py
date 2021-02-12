from copy import copy
from typing import List, Union

from src.player import Player
from src.unit_type import UnitType
from src.unit_type_resource import UnitTypeResource
from src.pow_modifier import POWModifier, filter_overdue_modifiers, get_final_pow, POWModifierKind


class Unit:
    """
    Класс, представляющий юнита на игровом поле.
    """

    def __init__(self, unit_type: Union[UnitType, type], owner: Player):
        """
        :param unit_type: Тип юнита.
        :param owner: Владелец юнита.
        """
        self._unit_type = unit_type
        self._modifiers = []
        self._owner = owner
        self._moving_points = self.get_default_moving_points()

    def reset_moving_points(self):
        self._moving_points = self.get_default_moving_points()

    def get_moving_points(self) -> int:
        return self._moving_points

    def get_default_moving_points(self) -> int:
        return self._unit_type.get_default_moving_points()

    def get_owner(self) -> Player:
        """
        Возвращает владельца юнита.
        """
        return self._owner

    def get_default_pow(self) -> int:
        """
        Возвращает дефолтное значение POW для данного типа юнитов.
        """
        return self._unit_type.get_default_pow()

    def get_all_modifiers(self) -> List[POWModifier]:
        """
        Возвращает все модификаторы, которые навешены в данный момент на юнита.
        :return: Список всех модификаторов, вне зависимости от их действия.
        """
        return copy(self._modifiers)

    def update_modifiers(self, current_turn: int):
        """
        Обновляет модификаторы, удаляя те, которые уже не действуют.
        :param current_turn: Номер текущего хода.
        """
        self._modifiers = list(filter_overdue_modifiers(current_turn, self._modifiers))

    def apply_modifier(self, modifier: POWModifier):
        """
        Применяет данный модификатор к юниту.
        :param modifier: Применяемый модификатор POW.
        """
        self._modifiers.append(modifier)

    def next_turn(self, current_turn: int):
        """
        Вызывается каждый ход для того, чтобы обновить вещи, зависимые от времени.
        """
        self.reset_moving_points()
        self.update_modifiers(current_turn)

    def after_attack(self):
        self._moving_points = 0

    def is_alive(self) -> bool:
        return self.count_pow() > 0

    def set_damage(self, damage: int, turn: int):
        self.apply_modifier(POWModifier(False, 2, turn, -damage, POWModifierKind.DAMAGE))

    def count_pow(self) -> int:
        return get_final_pow(self.get_default_pow(), self.get_all_modifiers())

    def count_priority(self) -> int:
        return self._unit_type.count_priority()

    def is_peaceful(self):
        return self._unit_type.is_peaceful()

    def decrease_moving_points(self, distance: int):
        self._moving_points -= distance

    def use_range_attack(self) -> bool:
        return self._unit_type.use_range_attack()

    def get_vision_radius(self) -> int:
        return self._unit_type.get_vision_radius()

    def get_resource(self) -> UnitTypeResource:
        """
        Возвращает ресурсы для визуализации юнита на поле.
        """
        return self._unit_type.get_resource()
