from .bot_request import Market
from constant import LONG, SHORT
from database.manager import Manager
from database.models import TickerDB, UnsuitableLevelsDB


class LevelDetector:
    @staticmethod
    def check_level(ticker, level, trend) -> bool:
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
    def check_levels(id, ticker, level, trend, **kwargs):
        def delete_unsuitable_lvl(id, ticker, level, trend):
            data = {
                'ticker': ticker, 'level': level, 'trend': trend
            }
            Manager.add_to_table(UnsuitableLevelsDB, data)
            Manager.delete_row(TickerDB, id)
        if trend == LONG and level < Market.get_mark_price(ticker):
            delete_unsuitable_lvl(id, ticker, level, trend)
        if trend == SHORT and level > Market.get_mark_price(ticker):
            delete_unsuitable_lvl(id, ticker, level, trend)
