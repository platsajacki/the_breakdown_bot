from pybit.unified_trading import WebSocket
import time
from param_position import Long  # , Short
from open_position import open_long
import keys
import example
import tg_bot


COEF_LEVEL_LONG = 0.9985
COEF_LEVEL_SHORT = 1.0015

session = WebSocket(
        testnet=True,
        api_key=keys.api_key,
        api_secret=keys.api_secret,
        channel_type='linear')


def check_long(symbol, mark_price, round_price):
    level = min(example.long_level[symbol])
    calc_level = level * COEF_LEVEL_LONG
    if calc_level < mark_price < level:
        a = Long(symbol, level, round_price)
        open_long(*a.get_param_position())


def handle_message(msg):
    symbol = msg['data']['symbol']
    mark_price = msg['data']['markPrice']
    round_price = len(mark_price.split('.')[1])
    if tg_bot.position == 'Long':
        check_long(symbol, float(mark_price), round_price)


if tg_bot.position == 'Long':
    for symbol in example.long_level:
        session.ticker_stream(symbol=symbol, callback=handle_message)


while True:
    time.sleep(1)
