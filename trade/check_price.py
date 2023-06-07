from pybit.unified_trading import WebSocket
from .param_position import Long, Short
from .bot_request import Market
from database.models import TickerDB, TrendDB
from database.manager import Manager

BUY: str = 'Buy'
SELL: str = 'Sell'
COEF_LEVEL_LONG: float = 0.9975
COEF_LEVEL_SHORT: float = 1.0025


connected_tickers = set()

session = WebSocket(testnet=True, channel_type='linear')


def check_long(symbol: str, mark_price: float, round_price: int):
    query = Manager.get_current_level(symbol[:-4], 'long')
    if query is not None:
        id, level = query['id'], query['level']
        calc_level: float = level * COEF_LEVEL_LONG
        if calc_level < mark_price < level:
            long_calc = Long(symbol, level, round_price)
            Market.open_pos(
                *long_calc.get_param_position(), BUY
            )
            Manager.delete_row(TickerDB, id)


def check_short(symbol: str, mark_price: float, round_price: int):
    query = Manager.get_current_level(symbol[:-4], 'short')
    if query is not None:
        id, level = query['id'], query['level']
        calc_level: float = level * COEF_LEVEL_SHORT
        if calc_level > mark_price > level:
            short_calc = Short(symbol, level, round_price)
            Market.open_pos(
                *short_calc.get_param_position(), SELL
            )
            Manager.delete_row(TickerDB, id)


def handle_message(msg):
    symbol = msg['data']['symbol']
    mark_price = msg['data']['markPrice']
    round_price = len(mark_price.split('.')[1])
    if Manager.get_row_by_id(TrendDB, 1).trend == 'long':
        check_long(symbol, float(mark_price), round_price)
    else:
        check_short(symbol, float(mark_price), round_price)


def connect_ticker(ticker) -> handle_message:
    connected_tickers.add(ticker)
    symbol = ticker + 'USDT'
    session.ticker_stream(symbol=symbol, callback=handle_message)


def start_check_tickers() -> connect_ticker:
    if Manager.get_row_by_id(TrendDB, 1).trend == 'long':
        for ticker in Manager.select_trend_tickers('long'):
            ticker = ticker[0]
            if ticker not in connected_tickers:
                connect_ticker(ticker)
    else:
        for ticker in Manager.select_trend_tickers('short'):
            ticker = ticker[0]
            if ticker not in connected_tickers:
                connect_ticker(ticker)
