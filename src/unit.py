"""
TODO: То, зачем это нужно.
"""

from copy import copy
from typing import List, Union

from src.unit_type import UnitType
from src.pow_modifier import POWModifier, filter_overdue_modifiers


class Unit:
    """
    Класс, представляющий юнита на игровом поле.
    """

    def __init__(self, unit_type: Union[UnitType, type]):
        """
        :param unit_type: Тип юнита.
        """
        self._unit_type = unit_type
        self._modifiers = []

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
        :param current_turn:
        """
        self.update_modifiers(current_turn)
