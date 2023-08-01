from .bot_request import Market
from constants import LONG, SHORT
from database.manager import Manager, transferring_row
from database.models import UnsuitableLevelsDB


class LevelDetector:
    @staticmethod
    def check_level(ticker: str, level: float, trend: str) -> bool:
        if trend == LONG:
            return (
                level > Market.get_mark_price(ticker)
                and level not in Manager.get_level_by_trend(ticker, trend)
            )
        else:
            return (
                level < Market.get_mark_price(ticker)
                and level not in Manager.get_level_by_trend(ticker, trend)
            )

    @staticmethod
    def check_levels(
        id: int, ticker: str, level: float, trend: str, **kwargs
    ) -> None:
        if trend == LONG and level < Market.get_mark_price(ticker):
            transferring_row(UnsuitableLevelsDB, id, ticker, level, trend)
        if trend == SHORT and level > Market.get_mark_price(ticker):
            transferring_row(UnsuitableLevelsDB, id, ticker, level, trend)
