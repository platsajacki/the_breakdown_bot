from decimal import Decimal
from typing import Any

from database.managers import RowManager, TickerManager
from database.models import UnsuitableLevels
from settings.constants import LONG, SHORT
from trade.requests import Market


class LevelDetector:
    """The class that checks for compliance with price requirements."""
    @staticmethod
    async def check_level(ticker: str, level: Decimal, trend: str) -> bool:
        """The method that checks the new levels for compliance when they are entered."""
        mark_price: Decimal = await Market.get_mark_price(ticker)
        return (
            (level > mark_price if trend == LONG else level < mark_price)
            and level not in await TickerManager.get_level_by_trend(ticker, trend)
        )

    @staticmethod
    async def check_levels(**kwargs: Any) -> None:
        """
        A method that checks the levels which
        are already written to the database for compliance.
        If they do not match, it deletes them.
        """
        mark_price: Decimal = (
            price
            if (price := kwargs.get('mark_price')) else
            await Market.get_mark_price(kwargs['ticker'])
        )
        if (
            kwargs['trend'] == LONG and kwargs['level'] < mark_price
            or kwargs['trend'] == SHORT and kwargs['level'] > mark_price
        ):
            await RowManager.transferring_row(
                UnsuitableLevels,
                kwargs['id'],
                kwargs['ticker'],
                kwargs['level'],
                kwargs['trend'],
                kwargs['median_price'],
                kwargs['update_median_price']
            )
