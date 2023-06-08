from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Position:
    '''The base class of positions'''
    symbol: str
    level: float
    round_price: int
    COEF_STOP: ClassVar[float] = 0.01
    COEF_LUFT: ClassVar[float] = 0.25
    COEF_TRIGGER_LONG: ClassVar[float] = 0.9985
    COEF_TRIGGER_SHORT: ClassVar[float] = 1.0015
    COEF_PROFIT: ClassVar[float] = 4

    def calculate_stop(self) -> float:
        calculatet_stop = self.level * self.COEF_STOP
        return calculatet_stop

    def calculate_luft(self) -> float:
        luft = self.calculate_stop() * self.COEF_LUFT
        return luft


class Long(Position):
    '''Calculation of a long position.'''
    def get_param_position(self) -> tuple[float]:
        entry_point = round(
            self.level + super().calculate_luft(), self.round_price
        )
        trigger = round(
            entry_point * self.COEF_TRIGGER_LONG, self.round_price
        )
        stop = round(
            entry_point - super().calculate_stop(), self.round_price
        )
        take_profit = round(
            entry_point + self.COEF_PROFIT * super().calculate_stop(),
            self.round_price
        )
        return self.symbol, entry_point, stop, take_profit, trigger


class Short(Position):
    '''Calculation of a short position.'''
    def get_param_position(self) -> tuple[float]:
        entry_point = round(
            self.level - super().calculate_luft(), self.round_price
        )
        trigger = round(
            entry_point * self.COEF_TRIGGER_SHORT, self.round_price
        )
        stop = round(
            entry_point + super().calculate_stop(), self.round_price
        )
        take_profit = round(
            entry_point - self.COEF_PROFIT * super().calculate_stop(),
            self.round_price
        )
        return self.symbol, entry_point, stop, take_profit, trigger
