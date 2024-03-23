import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from decimal import Decimal
from functools import partial
from typing import Any

from pybit.unified_trading import WebSocket

from database.managers import RowManager, TickerManager
from database.models import SpentLevelsDB, TrendDB, UnsuitableLevelsDB
from settings.config import CUSTOM_PING_INTERVAL, CUSTOM_PING_TIMEOUT, NOT_TESTNET
from settings.constants import (
    BUY,
    COEF_LEVEL_LONG,
    COEF_LEVEL_SHORT,
    LINEAR,
    LONG,
    POWER_RESERVE_USED_UP,
    SELL,
    SHORT,
    USDT,
)
from tg_bot.send_message import log_and_send_error, send_message
from tg_bot.text_message import InfoMessage
from trade.param_position import Long, Short
from trade.requests import Market
from trade.utils import handle_message_in_thread

logger = logging.getLogger(__name__)

connected_tickers: set[str] = set()
"""The list of connected tickers."""


async def get_ws_session_public() -> WebSocket:
    """Setup a connection WebSocket."""
    try:
        ws_session_public = WebSocket(testnet=NOT_TESTNET, channel_type=LINEAR)
        ws_session_public.ping_interval = CUSTOM_PING_INTERVAL
        ws_session_public.ping_timeout = CUSTOM_PING_TIMEOUT
        return ws_session_public
    except Exception as error:
        await log_and_send_error(logger, error, 'WebSocket `session_public`')


async def update_median_price_and_time(
    ticker: str, query: dict[str, int | Decimal | datetime], trend: str
) -> dict[str, int | Decimal | datetime]:
    TickerManager.set_median_price(id=query['id'], median_price=(await Market.get_median_price(ticker)))
    return TickerManager.get_current_level(ticker, trend)


async def check_long(ticker: str, mark_price: Decimal, round_price: int, *args: Any, **kwargs: Any) -> None:
    """Check for compliance with long positions. If the position fits the parameters, it opens an order."""
    if (query := TickerManager.get_current_level(ticker, LONG)) is not None:
        level: Decimal = query['level']
        if level < mark_price:
            RowManager.transferring_row(
                table=UnsuitableLevelsDB,
                id=query['id'],
                ticker=ticker,
                level=level,
                trend=LONG,
                median_price=query['median_price'],
                update_median_price=query['update_median_price'],
            )
            current_price_movement = await Market.get_current_price_movement(ticker)
            await send_message(
                InfoMessage.get_text_not_worked_out_level(ticker, level, query['median_price'], current_price_movement),
                kwargs['main_loop'],
            )
            return
        if query['median_price'] is None or datetime.now() - query['update_median_price'] > timedelta(days=1):
            query = await update_median_price_and_time(ticker, query, LONG)
        calc_level: Decimal = level * COEF_LEVEL_LONG
        if (
            calc_level < mark_price < level
            and (await Market.get_current_price_movement(ticker)) < query['median_price'] * POWER_RESERVE_USED_UP
        ):
            long_calc = Long(ticker, level, round_price)
            await Market.open_pos(*long_calc.get_param_position(), BUY, *args, **kwargs)
            RowManager.transferring_row(
                table=SpentLevelsDB,
                id=query['id'],
                ticker=ticker,
                level=level,
                trend=LONG,
                median_price=query['median_price'],
                update_median_price=query['update_median_price'],
            )


async def check_short(ticker: str, mark_price: Decimal, round_price: int, *args: Any, **kwargs: Any) -> None:
    """Check for compliance with short positions. If the position fits the parameters, it opens an order."""
    if (query := TickerManager.get_current_level(ticker, SHORT)) is not None:
        level: Decimal = query['level']
        if level > mark_price:
            RowManager.transferring_row(
                table=UnsuitableLevelsDB,
                id=query['id'],
                ticker=ticker,
                level=level,
                trend=SHORT,
                median_price=query['median_price'],
                update_median_price=query['update_median_price'],
            )
            current_price_movement = await Market.get_current_price_movement(ticker)
            await send_message(
                InfoMessage.get_text_not_worked_out_level(ticker, level, query['median_price'], current_price_movement),
                kwargs['main_loop'],
            )
            return
        if query['median_price'] is None or datetime.now() - query['update_median_price'] > timedelta(days=1):
            query = await update_median_price_and_time(ticker, query, SHORT)
        calc_level: Decimal = level * COEF_LEVEL_SHORT
        if (
            calc_level > mark_price > level
            and (await Market.get_current_price_movement(ticker)) < query['median_price'] * POWER_RESERVE_USED_UP
        ):
            short_calc = Short(ticker, level, round_price)
            await Market.open_pos(*short_calc.get_param_position(), SELL, *args, **kwargs)
            RowManager.transferring_row(
                table=SpentLevelsDB,
                id=query['id'],
                ticker=ticker,
                level=level,
                trend=SHORT,
                median_price=query['median_price'],
                update_median_price=query['update_median_price'],
            )


async def handle_message(msg: dict[str, Any], *args: Any, **kwargs: Any) -> None:
    """Stream message handler."""
    ticker: str = msg['data']['symbol'][:-4]
    mark_price_str: str = msg['data']['markPrice']
    round_price: int = len(mark_price_str.split('.')[1])
    mark_price = Decimal(mark_price_str)
    if RowManager.get_row_by_id(TrendDB, 1).trend == LONG:
        await check_long(ticker, mark_price, round_price, *args, **kwargs)
        return
    await check_short(ticker, mark_price, round_price, *args, **kwargs)


async def connect_ticker(ticker: str) -> None:
    """Connect the ticker to the stream."""
    connected_tickers.add(ticker)
    ws_session_public = await get_ws_session_public()
    with ThreadPoolExecutor() as executor:
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                executor,
                lambda: ws_session_public.ticker_stream(
                    symbol=f'{ticker}{USDT}',
                    callback=partial(handle_message_in_thread, coro=handle_message, main_loop=loop),
                ),
            )
        except Exception as error:
            await log_and_send_error(logger, error, f'`ticker_stream` {ticker}')


async def start_check_tickers() -> None:
    """Determine the direction of trade. Start the stream."""
    for ticker in TickerManager.get_tickers_by_trend(RowManager.get_row_by_id(TrendDB, 1).trend):
        if ticker[0] not in connected_tickers:
            await connect_ticker(ticker[0])
