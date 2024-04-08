import asyncio
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from functools import partial
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
        await asyncio.sleep(1)
        await TickerManager.set_median_price(id=id, median_price=(await Market.get_median_price(ticker)))
        return await TickerManager.get_current_level(ticker, trend)


async def check_long(ticker: str, mark_price: Decimal, round_price: int) -> None:
    """Check for compliance with long positions. If the position fits the parameters, it opens an order."""
    row = CONNECTED_TICKERS[ticker].get('row')
    if not CONNECTED_TICKERS[ticker]['price_movement']:
        return
    if not isinstance(row, Row):
        CONNECTED_TICKERS[ticker]['row'] = await TickerManager.get_current_level(ticker, LONG)
        await asyncio.sleep(WAITING_FOR_NEW_LEVEL)
        return
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
                ticker, row.level, CONNECTED_TICKERS[ticker].get('price_movement'), row.median_price
            )
        )
        return
    if row.median_price is None or datetime.now() - row.update_median_price > timedelta(days=1):
        CONNECTED_TICKERS[ticker]['row'] = await update_median_price_and_time(ticker, row.id, LONG)
        return
    if (
        row.level * COEF_LEVEL_LONG < mark_price < row.level
        and CONNECTED_TICKERS[ticker]['price_movement'] < row.median_price * POWER_RESERVE_USED_UP
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
    if not CONNECTED_TICKERS[ticker]['price_movement']:
        return
    if not isinstance(row, Row):
        CONNECTED_TICKERS[ticker]['row'] = await TickerManager.get_current_level(ticker, SHORT)
        await asyncio.sleep(WAITING_FOR_NEW_LEVEL)
        return
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
                ticker, row.level, CONNECTED_TICKERS[ticker].get('price_movement'), row.median_price
            )
        )
        return
    if row.median_price is None or datetime.now() - row.update_median_price > timedelta(days=1):
        CONNECTED_TICKERS[ticker]['row'] = await update_median_price_and_time(ticker, row.id, SHORT)
        return
    if (
        row.level * COEF_LEVEL_SHORT > mark_price > row.level
        and CONNECTED_TICKERS[ticker]['price_movement'] < row.median_price * POWER_RESERVE_USED_UP
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


async def handle_message_ticker(msg: dict[str, Any], ticker: str) -> None:
    """Stream message handler."""
    mark_price_str: str = msg['data']['markPrice']
    round_price: int = len(mark_price_str.split('.')[1]) if '.' in mark_price_str else 0
    if TREND['trend'] == LONG:
        await check_long(ticker, Decimal(mark_price_str), round_price)
        return
    await check_short(ticker, Decimal(mark_price_str), round_price)


async def handle_message_kline(msg: dict[str, Any], ticker: str) -> None:
    result = msg['data'][0]
    CONNECTED_TICKERS[ticker]['price_movement'] = Decimal(result['high']) - Decimal(result['low'])


async def connect_ticker(ticker: str) -> None:
    """Connect the ticker to the stream."""
    try:
        symbol = f'{ticker}{USDT}'
        (await get_ws_session_public()).ticker_stream(
            symbol=symbol,
            callback=partial(
                handle_message_coro,
                coro=handle_message_ticker,
                running_loop=asyncio.get_running_loop(),
                ticker=ticker,
            ),
        )
        await asyncio.sleep(0.1)
        (await get_ws_session_public()).kline_stream(
            symbol=symbol,
            interval='D',
            callback=partial(
                handle_message_coro,
                coro=handle_message_kline,
                running_loop=asyncio.get_running_loop(),
                ticker=ticker,
            ),
        )
        await asyncio.sleep(0.1)
    except Exception as error:
        await log_and_send_error(logger, error, f'`ticker_stream` {ticker}')


async def get_new_connected_ticker(ticker: str) -> ConnectedTicker:
    """Retrieve information about a new connected ticker."""
    return {
        'lock': asyncio.Lock(),
        'active_task': {
            'handle_message_ticker': False,
            'handle_message_kline': False,
        },
        'price_movement': None,
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
