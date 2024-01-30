import logging
from decimal import Decimal
from logging import config
from time import time
from typing import Any

from pybit.unified_trading import WebSocket

from bot_modules.send_message import log_and_send_error, send_message
from bot_modules.text_message import InfoMessage
from settings import (
    API_KEY,
    API_SECRET,
    BUY,
    CUSTOM_PING_INTERVAL,
    CUSTOM_PING_TIMEOUT,
    LINEAR,
    LOG_CONFIG,
    MINUTE_IN_MILLISECONDS,
    TESTNET,
)
from trade.bot_request import Market
from trade.param_position import Long, Short

config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)

# Setup a connection WebSocket.
try:
    session_privat = WebSocket(testnet=TESTNET, api_key=API_KEY, api_secret=API_SECRET, channel_type='private')
except Exception as error:
    log_and_send_error(logger, error, '`WebSocket session_privat`')


def handle_message(msg: dict[str, Any]) -> None:
    """The handler of messages about completed transactions. Check the trailing stop, if there is none, set."""
    for trade in msg['data']:
        exec_time: int = int(trade['execTime'])
        now_in_milliseconds: int = round(time() * 1000)
        if (
            now_in_milliseconds - exec_time < MINUTE_IN_MILLISECONDS
            and trade['category'] == LINEAR
        ):
            send_message(
                'Conducted trade '
                f'{InfoMessage.TRADE_MESSAGE.format(**trade)}'
            )
            symbol: str = trade['symbol']
            position_list: list[dict[str, Any]] | None = Market.get_open_positions(ticker=symbol[:-4])
            if position_list is None:
                send_message('The position is completely closed.')
                continue
            position: dict[str, Any] = position_list[0]
            if (
                Decimal(trade['closedSize']) == 0
                and Decimal(position['trailingStop']) == 0
            ):
                avg_price_str: str = position['avgPrice']
                round_price: int = (
                    len(avg_price_str.split('.')[1])
                    if '.' in avg_price_str
                    else 0
                )
                avg_price = Decimal(avg_price_str)
                if trade['side'] == BUY:
                    trailing_stop, active_price = Long.get_trailing_stop_param(avg_price, round_price)
                else:
                    trailing_stop, active_price = Short.get_trailing_stop_param(avg_price, round_price)
                Market.set_trailing_stop(
                    symbol, str(trailing_stop), str(active_price)
                )
                position['trailingStop'] = trailing_stop
            send_message(f'Total position {InfoMessage.POSITION_MESSAGE.format(**position)}')


def start_execution() -> None:
    session_privat.execution_stream(callback=handle_message)
    session_privat.ping_interval = CUSTOM_PING_INTERVAL
    session_privat.ping_timeout = CUSTOM_PING_TIMEOUT
