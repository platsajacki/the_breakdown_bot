from typing import Any

from pybit.unified_trading import WebSocket

from .bot_request import Market
from .param_position import Long, Short
from bot_modules.send_message import send_message
from bot_modules.text_message import InfoMessage
from constants import API_KEY, API_SECRET, CUSTOM_PING_INTERVAL, BUY

# Setup a connection WebSocket.
session_privat: WebSocket = WebSocket(
    testnet=True,
    api_key=API_KEY,
    api_secret=API_SECRET,
    channel_type='private'
)


def handle_message(msg: dict[str, Any]) -> None:
    """
    The handler of messages about completed transactions.
    Check the trailing stop, if there is none, set.
    """
    for trade in msg['data']:
        send_message(
            'Conducted trade - '
            f'{InfoMessage.TRADE_MESSAGE.format(**trade)}'
        )
        symbol: str = trade['symbol']
        position: list[dict[str, str]] | None = (
            Market.get_open_positions(ticker=symbol[:-4])
        )
        if position is None:
            send_message('The position is completely closed.')
            continue
        position: dict[str, str] = position[0]
        if (
            float(trade['closedSize']) == 0
            and float(position['trailingStop']) == 0
        ):
            avg_price: str = position['avgPrice']
            round_price: int = (
                len(avg_price.split('.')[1])
                if '.' in position['avgPrice']
                else 0
            )
            avg_price: float = float(avg_price)
            if trade['side'] == BUY:
                trailing_stop, active_price = (
                    Long.get_trailing_stop_param(avg_price, round_price)
                )
            else:
                trailing_stop, active_price = (
                    Short.get_trailing_stop_param(avg_price, round_price)
                )
            Market.set_trailing_stop(
                symbol, str(trailing_stop), str(active_price)
            )
        send_message(
            'Total position - '
            f'{InfoMessage.POSITION_MESSAGE.format(**position)}'
        )


def start_execution() -> None:
    session_privat.execution_stream(callback=handle_message)
    session_privat.ping_interval: int = CUSTOM_PING_INTERVAL
