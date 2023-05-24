from pybit.unified_trading import WebSocket
from .param_position import Long, Short
from .bot_request import open_pos
from database.modeles import TickerDB, TrendDB
import example

BUY: str = 'Buy'
SELL: str = 'Sell'
COEF_LEVEL_LONG: float = 0.9975
COEF_LEVEL_SHORT: float = 1.0025


connected_tickers = set()

session = WebSocket(
        testnet=True,
        channel_type='linear')


def check_long(symbol: str, mark_price: float, round_price: int):
    symbol_levels: list[int] = example.long_levels[symbol]
    print(symbol)
    if symbol_levels == []:
        pass
    else:
        level: float = min(symbol_levels)
        calc_level: float = level * COEF_LEVEL_LONG
        if calc_level < mark_price < level:
            long_calc = Long(symbol, level, round_price)
            open_pos(*long_calc.get_param_position(), BUY)
            symbol_levels.remove(level)


def check_short(symbol: str, mark_price: float, round_price: int):
    symbol_levels: list[int] = example.short_levels[symbol]
    print(symbol)
    if symbol_levels == []:
        pass
    else:
        level: float = max(symbol_levels)
        calc_level: float = level * COEF_LEVEL_SHORT
        if calc_level > mark_price > level:
            short_calc = Short(symbol, level, round_price)
            open_pos(*short_calc.get_param_position(), SELL)
            symbol_levels.remove(level)


def handle_message(msg):
    symbol = msg['data']['symbol']
    mark_price = msg['data']['markPrice']
    round_price = len(mark_price.split('.')[1])
    if example.trend == 'Long':
        check_long(symbol, float(mark_price), round_price)
    if example.trend == 'Short':
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
