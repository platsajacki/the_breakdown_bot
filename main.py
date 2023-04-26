'''The Breakdown Bot'''

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Position:
    '''The base class of positions'''
    ticket: str
    stop: float
    take_profit: float
    LUFT: ClassVar[float] = 0.25

    def count_entry_point(self) -> float:
        raise NotImplementedError('The method in the class '
                                  f'"{self.__class__.__name__}" '
                                  'is not defined.')

# 1
