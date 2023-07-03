from pybit.unified_trading import WebSocket

from .bot_request import Market
from .param_position import Long, Short
from constant import (
    BUY, COEF_LEVEL_LONG, COEF_LEVEL_SHORT, LINEAR, SELL, SHORT, USDT, LONG
)
from database.manager import Manager, transferring_row
from database.models import TrendDB, SpentLevelsDB


connected_tickers = set()

session = WebSocket(testnet=True, channel_type=LINEAR)


def check_long(symbol: str, mark_price: float, round_price: int):
    ticker = symbol[:-4]
    query = Manager.get_current_level(ticker, LONG)
    if query is not None:
        id, level = query['id'], query['level']
        calc_level: float = level * COEF_LEVEL_LONG
        if calc_level < mark_price < level:
            long_calc = Long(symbol, level, round_price)
            Market.open_pos(
                *long_calc.get_param_position(), BUY
            )
            transferring_row(
                table=SpentLevelsDB, id=id,
                ticker=ticker, level=level, trend=LONG
            )


def check_short(symbol: str, mark_price: float, round_price: int):
    ticker = symbol[:-4]
    query = Manager.get_current_level(ticker, SHORT)
    if query is not None:
        id, level = query['id'], query['level']
        calc_level: float = level * COEF_LEVEL_SHORT
        if calc_level > mark_price > level:
            short_calc = Short(symbol, level, round_price)
            Market.open_pos(
                *short_calc.get_param_position(), SELL
            )
            transferring_row(
                table=SpentLevelsDB, id=id,
                ticker=ticker, level=level, trend=SHORT
            )


def handle_message(msg):
    symbol = msg['data']['symbol']
    mark_price = msg['data']['markPrice']
    round_price = len(mark_price.split('.')[1])
    if Manager.get_row_by_id(TrendDB, 1).trend == LONG:
        check_long(symbol, float(mark_price), round_price)
    else:
        check_short(symbol, float(mark_price), round_price)


def connect_ticker(ticker):
    connected_tickers.add(ticker)
    symbol = f'{ticker}{USDT}'
    session.ticker_stream(symbol=symbol, callback=handle_message)


def start_check_tickers():
    if Manager.get_row_by_id(TrendDB, 1).trend == LONG:
        for ticker in Manager.select_trend_tickers(LONG):
            ticker = ticker[0]
            if ticker not in connected_tickers:
                connect_ticker(ticker)
    else:
        for ticker in Manager.select_trend_tickers(SHORT):
            ticker = ticker[0]
            if ticker not in connected_tickers:
                connect_ticker(ticker)
