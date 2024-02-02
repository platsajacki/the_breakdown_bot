import logging
from decimal import Decimal
from logging import config
from typing import Any

from aiohttp import ClientSession
from pybit.unified_trading import HTTP

from database.managers import RowManager
from database.models import OpenedOrderDB, StopVolumeDB
from settings import API_KEY, API_SECRET, BUY, CONTRACT, LINEAR, LOG_CONFIG, TESTNET, USDT
from tg_bot.send_message import log_and_send_error, send_message
from tg_bot.text_message import InfoMessage

config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)


async def get_session_http() -> HTTP:
    """Setup a connection with the exchange."""
    try:
        return HTTP(testnet=TESTNET, api_key=API_KEY, api_secret=API_SECRET)
    except Exception as error:
        await log_and_send_error(logger, error, '`session_http`')


class Market:
    """The class responsible for requests from the exchange."""
    @staticmethod
    async def get_symbol(ticker: str) -> str:
        """Check the symbol in the exchange listing."""
        url = f'https://api.bybit.com/v5/market/tickers?category={LINEAR}&symbol={ticker}{USDT}'  # noqa: E231
        async with ClientSession() as session:
            async with session.get(url) as response:
                return (await response.json())['retMsg']

    @staticmethod
    async def get_mark_price(ticker) -> Decimal:
        """Request for a ticker marking price."""
        info: dict[str, Any] = (await get_session_http()).get_tickers(category=LINEAR, symbol=f'{ticker}{USDT}')
        return Decimal(info['result']['list'][0]['markPrice'])

    @staticmethod
    async def open_pos(
        ticker: str, entry_point: Decimal, stop: Decimal, take_profit: Decimal,
        trigger: Decimal, side: str, *args: tuple, **kwargs: dict,
    ) -> None:
        """Round the position parameters and open it."""
        # Calculation of transaction volume
        session_http: HTTP = await get_session_http()
        min_order_qty: str = (
            session_http.get_instruments_info(
                category=LINEAR,
                symbol=(symbol := f'{ticker}{USDT}'))
            ['result']['list'][0]
            ['lotSizeFilter']['minOrderQty']
        )
        round_volume: int = len(min_order_qty.split('.')[1]) if '.' in min_order_qty else 0
        # Calculation of rounding.
        asset_volume = str(
            round((RowManager.get_row_by_id(StopVolumeDB, 1).usdt_volume / abs(entry_point - stop)), round_volume)
        )
        # Set up a trigger.
        triggerDirection: int = 1 if side == BUY else 2
        # Open an order.
        try:
            session_http.place_order(
                category=LINEAR,
                symbol=symbol,
                side=side,
                orderType='Limit',
                qty=asset_volume,
                tryggeBy='MarkPrice',
                triggerDirection=triggerDirection,
                triggerPrice=str(trigger),
                price=str(entry_point),
                takeProfit=str(take_profit),
                stopLoss=str(stop),
                orderFilter='Order'
            )
        except Exception as error:
            await log_and_send_error(logger, error, f'`place_order` {symbol} - {entry_point}', kwargs.get('main_loop'))
        open_order_params: dict[str, str | Decimal] = {
            'symbol': symbol,
            'asset_volume': asset_volume,
            'trigger': trigger,
            'entry_point': entry_point,
            'stop_loss': stop,
            'take_profit': take_profit
        }
        # Write the opened order to the table
        # and send a message about opening a position.
        RowManager.add_row(OpenedOrderDB, open_order_params)
        await send_message(InfoMessage.OPEN_ORDER_MESSAGE.format(**open_order_params), kwargs.get('main_loop'))

    @staticmethod
    async def get_wallet_balance() -> dict[str, Decimal]:
        """Request a wallet balance in USDT."""
        info: dict[str, Any] = (await get_session_http()).get_wallet_balance(accountType=CONTRACT, coin=USDT)
        coin: dict[str, Any] = info['result']['list'][0]['coin'][0]
        return {
            'equity': round(
                Decimal(coin['equity']), 2
            ),
            'unreal_pnl': round(
                Decimal(coin['unrealisedPnl']), 2
            ),
            'balance': round(
                Decimal(coin['walletBalance']), 2
            ),
            'real_pnl': round(
                Decimal(coin['cumRealisedPnl']), 2
            ),
        }

    @staticmethod
    async def get_open_orders(ticker: str) -> list[dict[str, str]] | None:
        """Request for open orders."""
        info: dict[str, Any] = (await get_session_http()).get_open_orders(symbol=f'{ticker}{USDT}', category=LINEAR)
        orders: list[dict[str, Any]] = info['result']['list']
        return None if orders == [] else orders

    @staticmethod
    async def get_open_positions(ticker: str) -> list[dict[str, str]] | None:
        """Request for open positions."""
        info = (await get_session_http()).get_positions(symbol=f'{ticker}{USDT}', category=LINEAR)
        positions: list[dict[str, Any]] = info['result']['list']
        return None if positions[0]['side'] == 'None' else positions

    @staticmethod
    async def set_trailing_stop(
        symbol: str, trailing_stop: str, active_price: str, *args: tuple, **kwargs: dict
    ) -> None:
        try:
            (await get_session_http()).set_trading_stop(
                symbol=symbol,
                category=LINEAR,
                trailingStop=trailing_stop,
                activePrice=active_price,
                positionIdx=0,
            )
        except Exception as error:
            await log_and_send_error(
                logger, error, f'`set_trading_stop` {symbol} - {active_price}', kwargs.get('main_loop')
            )
