from collections import namedtuple

from src.units.all import *


Cost = namedtuple('Cost', ['manpower', 'resources'])


COST_BY_TYPE = {
    IrregularType: Cost(100, 25),
    InfantryType: Cost(100, 75),
    DragoonType: Cost(75, 75),
    CuirassierType: Cost(75, 125),
    HussarType: Cost(75, 175),
    LightArtilleryType: Cost(50, 125),
    HeavyArtilleryType: Cost(50, 200)
}


NAME_BY_TYPE = {
    'Иррегуляры': IrregularType,
    'Пехота': InfantryType,
    'Драгуны': DragoonType,
    'Кирасиры': CuirassierType,
    'Гусары': HussarType,
    'Полевая артиллерия': LightArtilleryType,
    'Тяжелая артиллерия': HeavyArtilleryType
}

