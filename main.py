'''The Breakdown Bot'''

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Position:
    '''The base class of positions'''
    ticket: str
    level: float
    COEF_STOP: ClassVar[float] = 0.01
    COEF_LUFT: ClassVar[float] = 0.25
    COEF_PROFIT: ClassVar[float] = 4

    def calculate_stop(self) -> float:
        calculatet_stop = self.level * self.COEF_STOP
        return calculatet_stop

    def calculate_luft(self) -> float:
        luft = self.calculate_stop() * self.COEF_LUFT
        return luft


class Long(Position):
    '''Calculation of a long position.'''
    def get_param_position(self) -> float:
        entry_point = self.level + super().calculate_luft()
        stop = entry_point - super().calculate_stop()
        take_profit = entry_point + self.COEF_PROFIT * super().calculate_stop()
        print(super().calculate_stop(), super().calculate_luft(),
              entry_point, stop, take_profit)


class Short(Position):
    '''Calculation of a long position.'''
    def get_param_position(self) -> float:
        entry_point = self.level - super().calculate_luft()
        stop = entry_point + super().calculate_stop()
        take_profit = entry_point - self.COEF_PROFIT * super().calculate_stop()
        print(super().calculate_stop(), super().calculate_luft(),
              entry_point, stop, take_profit)
