import asyncio
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from functools import partial
from time import time
from typing import Any

from sqlalchemy import Row

from database.managers import RowManager, TickerManager
from database.models import SpentLevels, Trend, UnsuitableLevels
from database.temporary_data import CONNECTED_TICKERS, TREND
from settings.constants import (
    BUY,
    CHECK_MARK_BUTTON,
    COEF_LEVEL_LONG,
    COEF_LEVEL_SHORT,
    LONG,
    MINUTE_IN_MILLISECONDS,
    POWER_RESERVE_USED_UP,
    SELL,
    SHORT,
    USDT,
)
from settings.sessions import get_ws_session_public
from settings.types import ConnectedTicker
from tg_bot.send_message import log_and_send_error, send_message
from tg_bot.text_message import InfoMessage
from trade.param_position import Long, Short
from trade.requests import Market
from trade.utils import handle_message_coro

logger = logging.getLogger(__name__)

WAITING_FOR_NEW_LEVEL = 120


async def update_median_price_and_time(
    ticker: str, id: int, trend: str
) -> Row[tuple[int, Decimal, Decimal, datetime]] | None:
    """Update the median price and time for a given ticker and trend."""
    async with asyncio.Lock():
        await asyncio.sleep(0.1)
        await TickerManager.set_median_price(id=id, median_price=(await Market.get_median_price(ticker)))
        return await TickerManager.get_current_level(ticker, trend)


async def update_current_price_movement(ticker: str) -> None:
    """Updates the data for the current price movement of the specified ticker."""
    price_movement_time = CONNECTED_TICKERS[ticker]['price_movement'].get('time')
    now_in_milliseconds = int(time() * 1000)
    if isinstance(price_movement_time, int) and now_in_milliseconds - price_movement_time > MINUTE_IN_MILLISECONDS:
        CONNECTED_TICKERS[ticker]['price_movement']['time'] = now_in_milliseconds
        CONNECTED_TICKERS[ticker]['price_movement']['price'] = await Market.get_current_price_movement(ticker)


async def check_long(ticker: str, mark_price: Decimal, round_price: int) -> None:
    """Check for compliance with long positions. If the position fits the parameters, it opens an order."""
    row = CONNECTED_TICKERS[ticker].get('row')
    if not isinstance(row, Row):
        CONNECTED_TICKERS[ticker]['row'] = await TickerManager.get_current_level(ticker, LONG)
        await asyncio.sleep(WAITING_FOR_NEW_LEVEL)
        return
    await update_current_price_movement(ticker)
    if row.level < mark_price:
        await RowManager.transferring_row(
            table=UnsuitableLevels,
            id=row.id,
            ticker=ticker,
            level=row.level,
            trend=LONG,
            median_price=row.median_price,
            update_median_price=row.update_median_price,
        )
        CONNECTED_TICKERS[ticker]['row'] = await TickerManager.get_current_level(ticker, LONG)
        await send_message(
            InfoMessage.get_text_not_worked_out_level(
                ticker, row.level, CONNECTED_TICKERS[ticker]['price_movement'].get('price'), row.median_price
            )
        )
        return
    if row.median_price is None or datetime.now() - row.update_median_price > timedelta(days=1):
        row = await update_median_price_and_time(ticker, row.id, LONG)
        CONNECTED_TICKERS[ticker]['row'] = row
        return
    calc_level: Decimal = row.level * COEF_LEVEL_LONG
    if (
        calc_level < mark_price < row.level
        and CONNECTED_TICKERS[ticker]['price_movement']['price'] < row.median_price * POWER_RESERVE_USED_UP
    ):
        long_calc = Long(ticker, row.level, round_price)
        await Market.open_pos(*long_calc.get_param_position(), BUY)
        await RowManager.transferring_row(
            table=SpentLevels,
            id=row.id,
            ticker=ticker,
            level=row.level,
            trend=LONG,
            median_price=row.median_price,
            update_median_price=row.update_median_price,
        )
        CONNECTED_TICKERS[ticker]['row'] = await TickerManager.get_current_level(ticker, LONG)


async def check_short(ticker: str, mark_price: Decimal, round_price: int) -> None:
    """Check for compliance with short positions. If the position fits the parameters, it opens an order."""
    row = CONNECTED_TICKERS[ticker].get('row')
    if not isinstance(row, Row):
        CONNECTED_TICKERS[ticker]['row'] = await TickerManager.get_current_level(ticker, SHORT)
        await asyncio.sleep(WAITING_FOR_NEW_LEVEL)
        return
    await update_current_price_movement(ticker)
    if row.level > mark_price:
        await RowManager.transferring_row(
            table=UnsuitableLevels,
            id=row.id,
            ticker=ticker,
            level=row.level,
            trend=SHORT,
            median_price=row.median_price,
            update_median_price=row.update_median_price,
        )
        CONNECTED_TICKERS[ticker]['row'] = await TickerManager.get_current_level(ticker, SHORT)
        await send_message(
            InfoMessage.get_text_not_worked_out_level(
                ticker, row.level, CONNECTED_TICKERS[ticker]['price_movement'].get('price'), row.median_price
            )
        )
        return
    if row.median_price is None or datetime.now() - row.update_median_price > timedelta(days=1):
        row = await update_median_price_and_time(ticker, row.id, SHORT)
        CONNECTED_TICKERS[ticker]['row'] = row
        return
    calc_level: Decimal = row.level * COEF_LEVEL_SHORT
    if (
        calc_level > mark_price > row.level
        and CONNECTED_TICKERS[ticker]['price_movement']['price'] < row.median_price * POWER_RESERVE_USED_UP
    ):
        short_calc = Short(ticker, row.level, round_price)
        await Market.open_pos(*short_calc.get_param_position(), SELL)
        await RowManager.transferring_row(
            table=SpentLevels,
            id=row.id,
            ticker=ticker,
            level=row.level,
            trend=SHORT,
            median_price=row.median_price,
            update_median_price=row.update_median_price,
        )
        CONNECTED_TICKERS[ticker]['row'] = await TickerManager.get_current_level(ticker, SHORT)


async def handle_message(msg: dict[str, Any]) -> None:
    """Stream message handler."""
    ticker: str = msg['data']['symbol'][:-4]
    mark_price_str: str = msg['data']['markPrice']
    round_price: int = len(mark_price_str.split('.')[1]) if '.' in mark_price_str else 0
    if TREND['trend'] == LONG:
        await check_long(ticker, Decimal(mark_price_str), round_price)
        return
    await check_short(ticker, Decimal(mark_price_str), round_price)


async def connect_ticker(ticker: str) -> None:
    """Connect the ticker to the stream."""
    try:
        await asyncio.sleep(0.1)
        (await get_ws_session_public()).ticker_stream(
            symbol=f'{ticker}{USDT}',
            callback=partial(
                handle_message_coro,
                coro=handle_message,
                running_loop=asyncio.get_running_loop(),
                ticker=ticker,
            ),
        )
    except Exception as error:
        await log_and_send_error(logger, error, f'`ticker_stream` {ticker}')


async def get_new_connected_ticker(ticker: str) -> ConnectedTicker:
    """Retrieve information about a new connected ticker."""
    async with asyncio.Lock():
        await asyncio.sleep(0.1)
        return {
            'lock': asyncio.Lock(),
            'active_task': False,
            'price_movement': {
                'price': await Market.get_current_price_movement(ticker),
                'time': int(time() * 1000),
            },
            'row': await TickerManager.get_current_level(ticker, LONG),
        }


async def start_check_tickers() -> None:
    """Determine the direction of trade. Start the stream."""
    TREND['trend'] = (await RowManager.get_row_by_id(Trend, 1)).trend
    for ticker in await TickerManager.get_tickers_by_trend(TREND['trend']):
        if ticker not in CONNECTED_TICKERS:
            CONNECTED_TICKERS[ticker] = await get_new_connected_ticker(ticker)
            await connect_ticker(ticker)
    await send_message(f'All stickers are connected! {CHECK_MARK_BUTTON}')
