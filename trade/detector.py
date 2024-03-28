from decimal import Decimal

from database.managers import TickerManager
from settings.constants import LONG
from trade.requests import Market


class LevelDetector:
    """The class that checks for compliance with price requirements."""
    @staticmethod
    async def check_level(ticker: str, level: Decimal, trend: str) -> bool:
        """The method that checks the new levels for compliance when they are entered."""
        mark_price: Decimal = await Market.get_mark_price(ticker)
        return (
            (level > mark_price if trend == LONG else level < mark_price)
            and level not in await TickerManager.get_levels_by_ticker_and_trend(ticker, trend)
        )
