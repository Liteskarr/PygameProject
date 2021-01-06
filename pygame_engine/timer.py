"""
Модуль, предоставляющий интерфейс для взаимодействия кастомных
пользовательских ивентов с таймером.

Таймер реализован при помощи бинарной кучи.
"""

import heapq
from dataclasses import dataclass
from typing import List

import pygame


@dataclass
class TimerEvent:
    __slots__ = ('event', 'delta_time', 'initial_time', 'repeatable')

    event: pygame.event.Event
    delta_time: int
    initial_time: int
    repeatable: bool

    def is_ready(self, time: int):
        return time - self.initial_time >= self.delta_time

    def end_time(self):
        return self.initial_time + self.delta_time

    def __le__(self, other):
        return self.end_time() <= other.end_time()

    def __lt__(self, other):
        return self.end_time() < other.end_time()

    def __ge__(self, other):
        return self.end_time() >= other.end_time()

    def __gt__(self, other):
        return self.end_time() > other.end_time()


class Timer:
    def __init__(self):
        self._clock = pygame.time.Clock()
        self._heap = []

    def push(self, event: pygame.event.Event, delta_time: int, repeatable: bool = True):
        timer_event = TimerEvent(event, delta_time, self._clock.get_time(), repeatable)
        heapq.heappush(self._heap, timer_event)

    def top(self) -> TimerEvent:
        return self._heap[0]

    def pop(self) -> TimerEvent:
        if self.top().repeatable:
            top = self.top()
            self.push(top.event, top.delta_time, top.repeatable)
        return heapq.heappop(self._heap)

    def is_empty(self) -> bool:
        return not self._heap

    def get(self) -> List[pygame.event.Event]:
        events = []
        time = self._clock.get_time()
        while not self.is_empty() and self.top().is_ready(time):
            events.append(self.pop().event)
        return events
