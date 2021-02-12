from collections import namedtuple

from src.units.all import *


Cost = namedtuple('Cost', ['manpower', 'resources'])


COST_BY_TYPE = {
    IrregularType: Cost(100, 25),
}


NAME_BY_TYPE = {
    'Иррегуляры': IrregularType,
    'Пехота': int
}

