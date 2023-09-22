import logging as log
from typing import Any

from pybit.exceptions import InvalidChannelTypeError
from pybit.unified_trading import WebSocket

from .bot_request import Market
from .param_position import Long, Short
from bot_modules.send_message import send_message
from constants import (
    BUY, COEF_LEVEL_LONG, COEF_LEVEL_SHORT, LINEAR, LONG, SELL, SHORT, USDT,
    CUSTOM_PING_INTERVAL, CUSTOM_PING_TIMEOUT
)
from database.manager import Manager, transferring_row
from database.models import SpentLevelsDB, TrendDB

# The list of connected tickers.
connected_tickers: set[str] = set()

# Setup a connection WebSocket.
try:
    session_public: WebSocket = WebSocket(testnet=True, channel_type=LINEAR)
    session_public.ping_interval: int = CUSTOM_PING_INTERVAL
    session_public.ping_timeout: int = CUSTOM_PING_TIMEOUT
except InvalidChannelTypeError as error:
    log.error(error, exc_info=True)
    send_message(error)


def check_long(ticker: str, mark_price: float, round_price: int) -> None:
    """
    Check for compliance with long positions.
    If the position fits the parameters, it opens an order.
    """
    query: None | dict[str, int | float] = (
        Manager.get_current_level(ticker, LONG)
    )
    if query is not None:
        id: int = query['id']
        level: float = query['level']
        calc_level: float = level * COEF_LEVEL_LONG
        if calc_level < mark_price < level:
            long_calc = Long(ticker, level, round_price)
            Market.open_pos(
                *long_calc.get_param_position(), BUY
            )
            transferring_row(
                table=SpentLevelsDB, id=id,
                ticker=ticker, level=level, trend=LONG
            )


def check_short(ticker: str, mark_price: float, round_price: int) -> None:
    """
    Check for compliance with short positions.
    If the position fits the parameters, it opens an order.
    """
    query: None | dict[str, int | float] = (
        Manager.get_current_level(ticker, SHORT)
    )
    if query is not None:
        id: int = query['id']
        level: float = query['level']
        calc_level: float = level * COEF_LEVEL_SHORT
        if calc_level > mark_price > level:
            short_calc = Short(ticker, level, round_price)
            Market.open_pos(
                *short_calc.get_param_position(), SELL
            )
            transferring_row(
                table=SpentLevelsDB, id=id,
                ticker=ticker, level=level, trend=SHORT
            )


def handle_message(msg: dict[str, Any]) -> None:
    """Stream message handler."""
    ticker: str = msg['data']['symbol'][:-4]
    mark_price: str = msg['data']['markPrice']
    round_price: int = len(mark_price.split('.')[1])
    mark_price: float = float(mark_price)
    if Manager.get_row_by_id(TrendDB, 1).trend == LONG:
        check_long(ticker, mark_price, round_price)
    else:
        check_short(ticker, mark_price, round_price)


def connect_ticker(ticker) -> None:
    """Connect the ticker to the stream."""
    connected_tickers.add(ticker)
    try:
        session_public.ticker_stream(
            symbol=f'{ticker}{USDT}', callback=handle_message
        )
    except Exception as error:
        log.error(error, exc_info=True)
        send_message(error)


def start_check_tickers() -> None:
    """Determine the direction of trade. Start the stream."""
    if Manager.get_row_by_id(TrendDB, 1).trend == LONG:
        for ticker in Manager.select_trend_tickers(LONG):
            ticker: str = ticker[0]
            if ticker not in connected_tickers:
                connect_ticker(ticker)
    else:
        for ticker in Manager.select_trend_tickers(SHORT):
            ticker: str = ticker[0]
            if ticker not in connected_tickers:
                connect_ticker(ticker)
