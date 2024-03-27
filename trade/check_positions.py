import asyncio
import logging
from decimal import Decimal
from functools import partial
from time import time
from typing import Any

from settings.constants import BUY, LINEAR, MINUTE_IN_MILLISECONDS
from settings.sessions import get_ws_session_privat
from tg_bot.send_message import log_and_send_error, send_message
from tg_bot.text_message import InfoMessage
from trade.param_position import Long, Short
from trade.requests import Market
from trade.utils import handle_message_coro

logger = logging.getLogger(__name__)


async def handle_message(msg: dict[str, Any]) -> None:
    """The handler of messages about completed transactions. Check the trailing stop, if there is none, set."""
    for trade in msg['data']:
        exec_time = int(trade['execTime'])
        now_in_milliseconds = int(time() * 1000)
        if (
            now_in_milliseconds - exec_time < MINUTE_IN_MILLISECONDS
            and trade['category'] == LINEAR
        ):
            await send_message(f'Conducted trade {InfoMessage.TRADE_MESSAGE.format(**trade)}')
            symbol: str = trade['symbol']
            position_list: list[dict[str, Any]] | None = await Market.get_open_positions(ticker=symbol[:-4])
            if position_list is None:
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
            await send_message(txt)


async def start_execution_stream() -> None:
    """Start ws_session_privat.execution_stream."""
    try:
        (await get_ws_session_privat()).execution_stream(
            partial(handle_message_coro, coro=handle_message, running_loop=asyncio.get_running_loop())
        )
    except Exception as error:
        await log_and_send_error(logger, error, '`execution_stream`')
