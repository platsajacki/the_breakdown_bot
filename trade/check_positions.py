import asyncio
import logging
from asyncio import AbstractEventLoop
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from functools import partial
from time import time
from typing import Any

from pybit.unified_trading import WebSocket

from settings.config import API_KEY, API_SECRET, CUSTOM_PING_INTERVAL, CUSTOM_PING_TIMEOUT, NOT_TESTNET
from settings.constants import BUY, LINEAR, MINUTE_IN_MILLISECONDS
from tg_bot.send_message import log_and_send_error, send_message
from tg_bot.text_message import InfoMessage
from trade.param_position import Long, Short
from trade.requests import Market
from trade.utils import handle_message_in_thread

logger = logging.getLogger(__name__)


async def get_ws_session_privat() -> WebSocket:
    """Setup a connection WebSocket."""
    try:
        ws_session_privat = WebSocket(
            testnet=NOT_TESTNET, api_key=API_KEY, api_secret=API_SECRET, channel_type='private'
        )
        ws_session_privat.ping_interval = CUSTOM_PING_INTERVAL
        ws_session_privat.ping_timeout = CUSTOM_PING_TIMEOUT
        return ws_session_privat
    except Exception as error:
        await log_and_send_error(logger, error, '`WebSocket session_privat`')


async def handle_message(msg: dict[str, Any], *args: Any, **kwargs: AbstractEventLoop | Any) -> None:
    """The handler of messages about completed transactions. Check the trailing stop, if there is none, set."""
    for trade in msg['data']:
        exec_time = int(trade['execTime'])
        now_in_milliseconds: int = round(time() * 1000)
        if (
            now_in_milliseconds - exec_time < MINUTE_IN_MILLISECONDS
            and trade['category'] == LINEAR
        ):
            await send_message(f'Conducted trade {InfoMessage.TRADE_MESSAGE.format(**trade)}', kwargs.get('main_loop'))
            symbol: str = trade['symbol']
            position_list: list[dict[str, Any]] | None = await Market.get_open_positions(ticker=symbol[:-4])
            if position_list is None:
                await send_message('The position is completely closed.', kwargs.get('main_loop'))
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
                await Market.set_trailing_stop(
                    symbol, str(trailing_stop), str(active_price)
                )
                position['trailingStop'] = trailing_stop
            txt = (
                'The position is completely closed.'
                if Decimal(position['size']) == 0 else
                f'Total position {InfoMessage.POSITION_MESSAGE.format(**position)}'
            )
            await send_message(txt, kwargs.get('main_loop'))


async def start_execution_stream() -> None:
    """Start ws_session_privat.execution_stream."""
    ws_session_privat = await get_ws_session_privat()
    with ThreadPoolExecutor() as executor:
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                executor,
                ws_session_privat.execution_stream,
                partial(handle_message_in_thread, coro=handle_message, main_loop=loop),
            )
        except Exception as error:
            await log_and_send_error(logger, error, '`execution_stream`')
