"""
Аналог сигналов из Qt.
"""

from typing import Callable


class Signal:
    def __init__(self, *types):
        self._types = types
        self._listeners = []

    def emit(self, *args):
        for listener in self._listeners:
            listener(*args)

    def connect(self, listener: Callable):
        self._listeners.append(listener)

    def disconnect(self, listener_id: int):
        self._listeners.pop(list(map(id, self._listeners)).index(listener_id))

    def disconnect_all(self):
        self._listeners = []
