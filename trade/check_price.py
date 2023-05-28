from pybit.unified_trading import WebSocket
from .param_position import Long, Short
from .bot_request import open_pos
from database.models import TickerDB, TrendDB

BUY: str = 'Buy'
SELL: str = 'Sell'
COEF_LEVEL_LONG: float = 0.9975
COEF_LEVEL_SHORT: float = 1.0025


connected_tickers = set()

session = WebSocket(
        testnet=True,
        channel_type='linear')


def check_long(symbol: str, mark_price: float, round_price: int):
    query = TickerDB.get_min_long_lvl(symbol[:-4])
    if query is not None:
        id, level = query['id'], query['level']
        calc_level: float = level * COEF_LEVEL_LONG
        if calc_level < mark_price < level:
            long_calc = Long(symbol, level, round_price)
            open_pos(*long_calc.get_param_position(), BUY)
            TickerDB.delete_row(id)


def check_short(symbol: str, mark_price: float, round_price: int):
    query = TickerDB.get_max_short_lvl(symbol[:-4])
    if query is not None:
        id, level = query['id'], query['level']
        calc_level: float = level * COEF_LEVEL_SHORT
        if calc_level > mark_price > level:
            short_calc = Short(symbol, level, round_price)
            open_pos(*short_calc.get_param_position(), SELL)
            TickerDB.delete_row(id)


def handle_message(msg):
    symbol = msg['data']['symbol']
    mark_price = msg['data']['markPrice']
    round_price = len(mark_price.split('.')[1])
    if TrendDB.get_trend() == 'long':
        check_long(symbol, float(mark_price), round_price)
    if TrendDB.get_trend() == 'short':
        check_short(symbol, float(mark_price), round_price)


def connect_ticker(ticker):
    connected_tickers.add(ticker)
    symbol = ticker + 'USDT'
    session.ticker_stream(symbol=symbol, callback=handle_message)


def start_check_tickers():
    if TrendDB.get_trend() == 'long':
        for ticker in TickerDB.get_long_tickers():
            if ticker not in connected_tickers:
                connect_ticker(ticker)
    if TrendDB.get_trend() == 'short':
        for ticker in TickerDB.get_short_tickers():
            if ticker not in connected_tickers:
                connect_ticker(ticker)
