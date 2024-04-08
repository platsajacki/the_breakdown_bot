from dataclasses import dataclass
from decimal import Decimal
from typing import ClassVar


@dataclass
class Position:
    """The base class of positions."""
    ticker: str
    level: Decimal
    round_price: int
    COEF_STOP: ClassVar[Decimal] = Decimal('0.005')
    COEF_LUFT: ClassVar[Decimal] = Decimal('0.20')
    COEF_TRIGGER_LONG: ClassVar[Decimal] = Decimal('0.9995')
    COEF_TRIGGER_SHORT: ClassVar[Decimal] = Decimal('1.0005')
    COEF_PROFIT: ClassVar[Decimal] = Decimal('4')
    COEF_TRAILING_STOP: ClassVar[Decimal] = Decimal('0.00625')
    COEF_ACTIVE_PRICE: ClassVar[Decimal] = Decimal('0.0005')

    def calculate_stop(self) -> Decimal:
        """Calculation of the stop-loss."""
        return self.level * self.COEF_STOP

    def calculate_luft(self) -> Decimal:
        """
        Calculation of the luft.
        Luft - the distance from the level to the entry point
        to avoid opening on a false breakdown.
        """
        return self.calculate_stop() * self.COEF_LUFT

    @staticmethod
    def get_trailing_stop(avg_price: Decimal, round_price: int) -> Decimal:
        """Calculate the trailing stop."""
        return round(avg_price * Position.COEF_TRAILING_STOP, round_price)


class Long(Position):
    """The class represents a position based on price growth."""
    def get_param_position(self) -> tuple[str, Decimal, Decimal, Decimal, Decimal]:
        """Calculation of a long position."""
        entry_point: Decimal = round(
            self.level + super().calculate_luft(), self.round_price
        )
        trigger: Decimal = round(
            entry_point * self.COEF_TRIGGER_LONG, self.round_price
        )
        stop: Decimal = round(
            entry_point - super().calculate_stop(), self.round_price
        )
        take_profit: Decimal = round(
            entry_point + self.COEF_PROFIT * super().calculate_stop(), self.round_price
        )
        return self.ticker, entry_point, stop, take_profit, trigger

    @staticmethod
    def get_trailing_stop_param(avg_price: Decimal, round_price: int) -> tuple[Decimal, Decimal]:
        """Calculate the trailing stop parameters for a long position."""
        trailing_stop: Decimal = Long.get_trailing_stop(avg_price, round_price)
        active_price: Decimal = round(avg_price + avg_price * Long.COEF_ACTIVE_PRICE, round_price)
        return trailing_stop, active_price


class Short(Position):
    """The class represents a position based on declining price."""
    def get_param_position(self) -> tuple[str, Decimal, Decimal, Decimal, Decimal]:
        """Calculation of a short position."""
        entry_point: Decimal = round(
            self.level - super().calculate_luft(), self.round_price
        )
        trigger: Decimal = round(
            entry_point * self.COEF_TRIGGER_SHORT, self.round_price
        )
        stop: Decimal = round(
            entry_point + super().calculate_stop(), self.round_price
        )
        take_profit: Decimal = round(
            entry_point - self.COEF_PROFIT * super().calculate_stop(),
            self.round_price
        )
        return self.ticker, entry_point, stop, take_profit, trigger

    @staticmethod
    def get_trailing_stop_param(avg_price: Decimal, round_price: int) -> tuple[Decimal, Decimal]:
        """Calculate the trailing stop parameters for a short position."""
        trailing_stop: Decimal = Short.get_trailing_stop(avg_price, round_price)
        active_price: Decimal = round(avg_price - avg_price * Short.COEF_ACTIVE_PRICE, round_price)
        return trailing_stop, active_price
