from time import sleep
from pybit.unified_trading import WebSocket
from param_position import Long, Short
from open_position import open_pos
import keys
import example
import tg_bot

BUY: str = 'Buy'
SELL: str = 'Sell'
COEF_LEVEL_LONG: float = 0.9975
COEF_LEVEL_SHORT: float = 1.0025

session = WebSocket(
        testnet=True,
        api_key=keys.api_key,
        api_secret=keys.api_secret,
        channel_type='linear')


def check_long(symbol, mark_price, round_price) -> open_pos():
    symbol_levels = example.long_levels[symbol]
    if symbol_levels is None:
        pass
    else:
        level = min(symbol_levels)
        calc_level = level * COEF_LEVEL_LONG
        if calc_level < mark_price < level:
            long_calc = Long(symbol, level, round_price)
            open_pos(*long_calc.get_param_position(), BUY)
            symbol_levels.remove(level)
            example.long_levels[symbol] = symbol_levels


def check_short(symbol, mark_price, round_price) -> open_pos():
    symbol_levels = example.long_levels[symbol]
    if symbol_levels is None:
        pass
    else:
        level = max(symbol_levels)
        calc_level = level * COEF_LEVEL_SHORT
        if calc_level > mark_price > level:
            short_calc = Short(symbol, level, round_price)
            open_pos(*short_calc.get_param_position(), SELL)
            symbol_levels.remove(level)
            example.long_levels[symbol] = symbol_levels


def handle_message(msg):
    symbol = msg['data']['symbol']
    mark_price = msg['data']['markPrice']
    round_price = len(mark_price.split('.')[1])
    if tg_bot.position == 'Long':
        check_long(symbol, float(mark_price), round_price)
    if tg_bot.position == 'Short':
        check_short(symbol, float(mark_price), round_price)


for symbol in example.long_levels:
    session.ticker_stream(symbol=symbol, callback=handle_message)


while True:
    sleep(0.5)
