import asyncio
import json
import logging
from datetime import datetime, timedelta
from subprocess import PIPE, Popen

from settings.constants import LINEAR
from tg_bot.send_message import log_and_send_error
from trade.sessions import get_session_http

logger = logging.getLogger(__name__)


async def get_all_linear_symbols() -> list[str]:
    """Retrieves a list of all linear symbols."""
    result = (await get_session_http()).get_instruments_info(category=LINEAR)['result']['list']
    symbols = []
    for symbol_data in result:
        symbol = symbol_data['symbol']
        if '1000'not in symbol and '-' not in symbol:
            symbols.append(symbol)
    return symbols


async def get_all_klines(symbols: list[str], interval: str = 'D') -> dict:
    """Retrieves all klines for the given symbols."""
    http_session = await get_session_http()
    start_time = int(datetime(2018, 1, 1).timestamp()) * 1000
    end_time = int((datetime.now() - timedelta(days=1)).timestamp()) * 1000
    symbols_klines = dict()

    async def get_kline(symbol, interval=interval):
        result = http_session.get_kline(
            category=LINEAR,
            symbol=symbol,
            interval=interval,
            start=start_time,
            end=end_time,
            limit=1000,
        )['result']['list']
        symbols_klines[symbol] = result

    await asyncio.gather(*[get_kline(symbol, interval) for symbol in symbols])
    return symbols_klines


async def get_all_levels() -> None | dict[str, dict[str, int]]:
    """Retrieves all levels for all symbols."""
    all_klines = await get_all_klines(await get_all_linear_symbols())
    process = Popen(
        ['trade/calculateLevels'],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        text=True,
    )
    stdout, stderr = process.communicate(input=json.dumps(all_klines))
    if 'panic:' in stderr:
        await log_and_send_error(logger, Exception(stderr))
        return None
    return json.loads(stdout)
