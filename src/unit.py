from copy import copy
from typing import List, Union

from src.player import Player
from src.unit_type import UnitType
from src.unit_type_resource import UnitTypeResource
from src.pow_modifier import POWModifier, filter_overdue_modifiers


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
        self.update_modifiers(current_turn)

    def get_resource(self) -> UnitTypeResource:
        """
        Возвращает ресурсы для визуализации юнита на поле.
        """
        return self._unit_type.get_resource()
