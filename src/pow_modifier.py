from typing import Iterable
from enum import Enum, auto
from dataclasses import dataclass


class POWModifierKind(Enum):
    DAMAGE = auto()
    TERRAIN = auto()


@dataclass
class POWModifier:
    kind: POWModifierKind
    duration: int
    value: int


def get_result(base: int, modifiers: Iterable[POWModifier]) -> int:
    return base + sum(map(lambda x: x.value, modifiers))
