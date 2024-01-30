from decimal import Decimal

from database.manager import Manager, transferring_row
from database.models import UnsuitableLevelsDB
from settings import LONG, SHORT
from trade.bot_request import Market


class LevelDetector:
    """The class that checks for compliance with price requirements."""
    @staticmethod
    def check_level(ticker: str, level: Decimal, trend: str) -> bool:
        """The method that checks the new levels for compliance when they are entered."""
        if trend == LONG:
            return level > Market.get_mark_price(ticker) and level not in Manager.get_level_by_trend(ticker, trend)
        else:
            return level < Market.get_mark_price(ticker) and level not in Manager.get_level_by_trend(ticker, trend)

    @staticmethod
    def check_levels(id: int, ticker: str, level: Decimal, trend: str, **kwargs) -> None:
        """
        A method that checks the levels which
        are already written to the database for compliance.
        If they do not match, it deletes them.
        """
        if trend == LONG and level < Market.get_mark_price(ticker):
            transferring_row(UnsuitableLevelsDB, id, ticker, level, trend)
        if trend == SHORT and level > Market.get_mark_price(ticker):
            transferring_row(UnsuitableLevelsDB, id, ticker, level, trend)
