"""
На POW действуют различные модификаторы. Для того, чтобы отлавливать и изменять конкретные, такое
необходимо, например, лидерам, все модификаторы классифицируются.
Некоторые модификаторы действуют несколько ходов или до определенного события.
"""

from typing import Iterable
from enum import Enum, auto
from dataclasses import dataclass


class POWModifierKind(Enum):
    """
    Перечисление всех игровых модификаторов.
    """
    # Модификатор, не имеющий конкретного типа, но существующий.
    NONE = auto()
    # Урон, полученный за предыдущие битвы.
    DAMAGE = auto()
    # Модификатор местности.
    TERRAIN = auto()
    # Модификатор биома.
    BIOME = auto()
    # Модификатор защиты.
    DEFENCIVE = auto()
    # Модификатор атаки
    ATTACKING = auto()
    # Модификатор дезорганизации.
    DISORGANIZATION = auto()


@dataclass
class POWModifier:
    """
    Класс-контейнер для данных модификатора.
    """

    eternal: bool
    duration: int
    from_turn: int
    value: int
    kind: POWModifierKind = POWModifierKind.NONE

    def is_valid(self, current_turn: int) -> bool:
        """
        Проверяет, действует ли модификатор на текущем ходу.
        Модификатор оказывает свое действие, начиная с хода применения.
        :param current_turn: Текущий ход.
        :return: True, если действует, иначе False.
        """
        return current_turn - self.from_turn + 1 <= self.duration or self.eternal


class NonePOWModifier(POWModifier):
    """
    Класс-заглушка для пустых модификаторов, которые могут быть использованы в некоторых классах.
    """

    eternal: bool = False
    duration: int = 0
    from_turn: int = 0
    value: int = 0
    kind: POWModifierKind = POWModifierKind.NONE

    def __init__(self):
        """
        Делает необязательным указание значений в инициализаторе.
        """
        pass

    def is_valid(self, current_turn: int) -> bool:
        return False


def filter_overdue_modifiers(current_turn: int, modifiers: Iterable[POWModifier]) -> Iterable[POWModifier]:
    """
    Отфильтровывает недействительные модификаторы.
    :param current_turn: Текущий ход.
    :param modifiers: Перечисление модификаторов.
    :return: Итератор на действующие модификаторы.
    """
    for modifier in modifiers:
        if modifier.is_valid(current_turn):
            yield modifier


def get_final_pow(base: int, modifiers: Iterable[POWModifier]) -> int:
    """
    Быстрый расчет итогового POW юнита.
    :param base: Базовый POW юнита.
    :param modifiers: Перечисление модификаторов, которые оказывают действие на юнит.
    :return: Итоговый POW юнита.
    """
    return base + sum(map(lambda x: x.value, modifiers))
