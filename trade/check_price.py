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
from settings.constants import BUY, COEF_LEVEL_LONG, COEF_LEVEL_SHORT, LONG, POWER_RESERVE_USED_UP, SELL, SHORT, USDT
from settings.sessions import get_ws_session_public
from tg_bot.send_message import log_and_send_error, send_message
from tg_bot.text_message import InfoMessage
from trade.param_position import Long, Short
from trade.requests import Market
from trade.utils import handle_message_coro

logger = logging.getLogger(__name__)


async def update_median_price_and_time(
    ticker: str, id: int, trend: str
) -> Row[tuple[int, Decimal, Decimal, datetime]] | None:
    """Update the median price and time for a given ticker and trend."""
    await TickerManager.set_median_price(id=id, median_price=(await Market.get_median_price(ticker)))
    return await TickerManager.get_current_level(ticker, trend)


async def check_long(ticker: str, mark_price: Decimal, round_price: int) -> None:
    """Check for compliance with long positions. If the position fits the parameters, it opens an order."""
    row = CONNECTED_TICKERS[ticker].get('row')
    if isinstance(row, Row):
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
            CONNECTED_TICKERS[ticker]['row'] = None
            current_price_movement = await Market.get_current_price_movement(ticker)
            await send_message(
                InfoMessage.get_text_not_worked_out_level(
                    ticker, row.level, row.median_price, current_price_movement
                )
            )
            return
        if row.median_price is None or datetime.now() - row.update_median_price > timedelta(days=1):
            row = await update_median_price_and_time(ticker, row.id, LONG)
            CONNECTED_TICKERS[ticker]['row'] = row
            if row is None:
                return
        calc_level: Decimal = row.level * COEF_LEVEL_LONG
        if (
            calc_level < mark_price < row.level
            and (await Market.get_current_price_movement(ticker)) < row.median_price * POWER_RESERVE_USED_UP
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
            CONNECTED_TICKERS[ticker]['row'] = None


async def check_short(ticker: str, mark_price: Decimal, round_price: int) -> None:
    """Check for compliance with short positions. If the position fits the parameters, it opens an order."""
    row = CONNECTED_TICKERS[ticker].get('row')
    if isinstance(row, Row):
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
            current_price_movement = await Market.get_current_price_movement(ticker)
            await send_message(
                InfoMessage.get_text_not_worked_out_level(
                    ticker, row.level, row.median_price, current_price_movement
                )
            )
            return
        if row.median_price is None or datetime.now() - row.update_median_price > timedelta(days=1):
            row = await update_median_price_and_time(ticker, row.id, SHORT)
            CONNECTED_TICKERS[ticker]['row'] = row
            if row is None:
                return
        calc_level: Decimal = row.level * COEF_LEVEL_SHORT
        if (
            calc_level > mark_price > row.level
            and (await Market.get_current_price_movement(ticker)) < row.median_price * POWER_RESERVE_USED_UP
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
            CONNECTED_TICKERS[ticker]['row'] = None


async def handle_message(msg: dict[str, Any]) -> None:
    """Stream message handler."""
    ticker: str = msg['data']['symbol'][:-4]
    mark_price_str: str = msg['data']['markPrice']
    round_price: int = len(mark_price_str.split('.')[1]) if '.' in mark_price_str else 0
    mark_price = Decimal(mark_price_str)
    if TREND['trend'] == LONG:
        await check_long(ticker, mark_price, round_price)
        return
    await check_short(ticker, mark_price, round_price)


async def connect_ticker(ticker: str) -> None:
    """Connect the ticker to the stream."""
    try:
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


async def start_check_tickers() -> None:
    """Determine the direction of trade. Start the stream."""
    TREND['trend'] = (await RowManager.get_row_by_id(Trend, 1)).trend
    # for ticker in await TickerManager.get_tickers_by_trend(TREND['trend']):
    for ticker in ['BTC']:
        if ticker not in CONNECTED_TICKERS:
            CONNECTED_TICKERS[ticker] = {}
            CONNECTED_TICKERS[ticker]['row'] = await TickerManager.get_current_level(ticker, LONG)
            await connect_ticker(ticker)
