import asyncio
from datetime import datetime, timedelta
from logging import DEBUG as LOGGING_DEBUG
from logging import basicConfig

from settings.constants import LINEAR
from trade.sessions import get_session_http

basicConfig(level=LOGGING_DEBUG)


async def get_all_linear_symbols() -> list[str]:
    result = (await get_session_http()).get_instruments_info(category=LINEAR)['result']['list']
    symbols = []
    for symbol_data in result:
        symbol = symbol_data['symbol']
        if '1000'not in symbol and '-' not in symbol:
            symbols.append(symbol)
    return symbols


async def get_all_klines(symbols: list[str], interval: str = 'D') -> dict:
    http_session = await get_session_http()
    start_time = int(datetime(2018, 1, 1).timestamp()) * 1000
    end_time = int((datetime.now() - timedelta(days=1)).timestamp()) * 1000
    symbols_klines = dict()

    async def get_kline(symbol, interval=interval) -> dict:
        result = http_session.get_kline(
            category=LINEAR,
            symbol=symbol,
            interval=interval,
            start=start_time,
            end=end_time,
        )['result']['list']
        symbols_klines[symbol] = result

    await asyncio.gather(*[get_kline(symbol, interval) for symbol in symbols])
    return symbols_klines
