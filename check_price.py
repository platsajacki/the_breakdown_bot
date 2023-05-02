from pybit.unified_trading import WebSocket
from time import sleep
import keys
import example

COEF_LEVEL_LONG = 0.9975
COEF_LEVEL_SHORT = 1.0025


'''Initialise the session.'''
session = WebSocket(
    testnet=True,
    api_key=keys.api_key,
    api_secret=keys.api_secret,
    channel_type='linear')
session._connect(url='wss://stream-testnet.bybit.com/v5/public/linear')

#  Long НАДО ПОНЯТЬ, как передать левел корректно
for ticket, level in example.data.items():
    session.ticker_stream(symbol=f'{ticket}USDT',
                          callback=lambda msg, level=level:
                          handle_message(msg, level))


def handle_message(msg, level):
    mark_price = float(msg['data']['markPrice'])
    symbol = msg['data']['symbol']
    calc_level = level * COEF_LEVEL_LONG
    if calc_level < mark_price < level:
        print(symbol, mark_price)


while True:
    sleep(3)
