"""
# TODO: То, почему этот класс требуется в коде.
"""

from src.unit_group import UnitGroup


def is_group(group: type):
    """
    Проверяет, является ли группа наследником от UnitGroup.
    :return: True, если является, иначе False.
    """
    return issubclass(group, UnitGroup)


class UnitGroupsContainer:
    """
    Реализует хранение, добавление, удаление и поиск групп юнита.
    """
    def __init__(self):
        self._groups = set()

    def add(self, group: type):
        """
        Добавляет данную группу в контейнер.
        """
        if is_group(group):
            self._groups.add(group)

    def delete(self, group: type):
        """
        Удаляет данную группу из контейнера.
        """
        if is_group(group):
            self._groups.remove(group)

    def contains(self, group: type) -> bool:
        """
        Проверяет, находится ли данная группа в контейнере.
        :return: True, если находится, иначе False.
        """
        if is_group(group):
            return group in self._groups
