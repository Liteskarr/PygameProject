"""
Описание логики игрового процесса.
"""

from src.world_map import WorldMap
from src.units_manager import UnitsManager


class Game:
    """
    Класс, объединяющий все классы взаимодействия с игровым процессом.
    """

    def __init__(self):
        self._current_turn = 1

    def load_from_file(self, filepath: str):
        """
        Загружает игру из файла в данный объект.
        :param filepath: Путь к файлу.
        """
        pass

    def save_to_file(self, filepath: str):
        """
        Сохраняет игру в файл из данного объекта.
        :param filepath: Путь к файлу.
        """
        pass

    def next_turn(self):
        """
        Определяет игровое поведение при смене хода.
        """
        self._current_turn += 1

    def get_current_turn(self) -> int:
        """
        Возвращает номер текущего хода.
        :return:
        """
        return self._current_turn

    def set_map(self, world_map: WorldMap):
        """"
        Устанавливает карту мира на поле.
        """
        self._world_map = world_map

    def get_map(self) -> WorldMap:
        """
        Возвращает игровую карту.
        """
        return self._world_map

    def set_units_manager(self, units_manager: UnitsManager):
        """
        Устанавливает текущий менеджер юнитов.
        """
        self._units_manager = units_manager

    def get_units_manager(self) -> UnitsManager:
        """
        Возвращает текущий менеджер юнитов.
        """
        return self._units_manager
