from decimal import Decimal

from database.managers import RowManager, TickerManager
from database.models import UnsuitableLevelsDB
from settings import LONG, SHORT
from trade.requests import Market


class LevelDetector:
    """The class that checks for compliance with price requirements."""
    @staticmethod
    async def check_level(ticker: str, level: Decimal, trend: str) -> bool:
        """The method that checks the new levels for compliance when they are entered."""
        mark_price: Decimal = await Market.get_mark_price(ticker)
        return (
            (level > mark_price if trend == LONG else level < mark_price)
            and level not in TickerManager.get_level_by_trend(ticker, trend)
        )

    @staticmethod
    async def check_levels(id: int, ticker: str, level: Decimal, trend: str, **kwargs) -> None:
        """
        A method that checks the levels which
        are already written to the database for compliance.
        If they do not match, it deletes them.
        """
        mark_price: Decimal = await Market.get_mark_price(ticker)
        if trend == LONG and level < mark_price:
            RowManager.transferring_row(UnsuitableLevelsDB, id, ticker, level, trend)
        if trend == SHORT and level > mark_price:
            RowManager.transferring_row(UnsuitableLevelsDB, id, ticker, level, trend)
