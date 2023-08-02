from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Position:
    """The base class of positions."""
    symbol: str
    level: float
    round_price: int
    COEF_STOP: ClassVar[float] = 0.01
    COEF_LUFT: ClassVar[float] = 0.25
    COEF_TRIGGER_LONG: ClassVar[float] = 0.9995
    COEF_TRIGGER_SHORT: ClassVar[float] = 1.0005
    COEF_PROFIT: ClassVar[float] = 4

    def calculate_stop(self) -> float:
        """Calculation of the stop-loss."""
        calculatet_stop: float = self.level * self.COEF_STOP
        return calculatet_stop

    def calculate_luft(self) -> float:
        """
        Calculation of the luft.
        Luft - the distance from the level to the entry point
        to avoid opening on a false breakdown.
        """
        luft: float = self.calculate_stop() * self.COEF_LUFT
        return luft


class Long(Position):
    """The class represents a position based on price growth."""
    def get_param_position(self) -> tuple[str, float, float, float, float]:
        """Calculation of a long position."""
        entry_point: float = round(
            self.level + super().calculate_luft(), self.round_price
        )
        trigger: float = round(
            entry_point * self.COEF_TRIGGER_LONG, self.round_price
        )
        stop: float = round(
            entry_point - super().calculate_stop(), self.round_price
        )
        take_profit: float = round(
            entry_point + self.COEF_PROFIT * super().calculate_stop(),
            self.round_price
        )
        return self.symbol, entry_point, stop, take_profit, trigger


class Short(Position):
    """The class represents a position based on declining price."""
    def get_param_position(self) -> tuple[str, float, float, float, float]:
        """Calculation of a short position."""
        entry_point: float = round(
            self.level - super().calculate_luft(), self.round_price
        )
        trigger: float = round(
            entry_point * self.COEF_TRIGGER_SHORT, self.round_price
        )
        stop: float = round(
            entry_point + super().calculate_stop(), self.round_price
        )
        take_profit: float = round(
            entry_point - self.COEF_PROFIT * super().calculate_stop(),
            self.round_price
        )
        return self.symbol, entry_point, stop, take_profit, trigger
