import logging as log
from typing import Any

from pybit.exceptions import InvalidRequestError
from pybit.unified_trading import HTTP
from requests import get

from bot_modules.send_message import send_message
from bot_modules.text_message import InfoMessage
from constants import API_KEY, API_SECRET, BUY, CONTRACT, LINEAR, USDT
from database.manager import Manager
from database.models import OpenedOrderDB, StopVolumeDB
from exceptions import HTTPSessionError

# Setup a connection with the exchange.
try:
    session_http: HTTP = HTTP(
        testnet=True,
        api_key=API_KEY,
        api_secret=API_SECRET
    )
except HTTPSessionError as error:
    log.error(error, exc_info=True)
    send_message(error)


class Market:
    """The class responsible for requests from the exchange."""
    @staticmethod
    def get_symbol(ticker: str) -> str:
        """Check the symbol in the exchange listing."""
        url: str = (
            'https://api.bybit.com/'
            f'v5/market/tickers?category={LINEAR}&symbol={ticker}{USDT}'
        )
        return get(url).json()['retMsg']

    @staticmethod
    def get_mark_price(ticker) -> float:
        """Request for a ticker marking price."""
        info: dict[str, Any] = session_http.get_tickers(
            category=LINEAR, symbol=f'{ticker}{USDT}'
        )
        mark_price: float = float(info['result']['list'][0]['markPrice'])
        return mark_price

    @staticmethod
    def open_pos(symbol: str, entry_point: float, stop: float,
                 take_profit: float, trigger: float, side: str) -> None:
        """Round the position parameters and open it."""
        # Calculation of transaction volume
        min_order_qty: str = (
            session_http.get_instruments_info(
                category=LINEAR,
                symbol=symbol)
            ['result']['list'][0]
            ['lotSizeFilter']['minOrderQty']
        )
        round_volume: int = (
            len(min_order_qty.split('.')[1])
            if '.' in min_order_qty
            else 0
        )
        # Calculation of rounding.
        asset_volume: str = (
            str(round(
                (Manager.get_row_by_id(StopVolumeDB, 1).usdt_volume
                 / abs(entry_point - stop)), round_volume))
        )
        # Set up a trigger.
        if side == BUY:
            triggerDirection: int = 1
        else:
            triggerDirection: int = 2
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
        except InvalidRequestError as error:
            send_message(error)
        open_order_params: dict[str, str | float] = {
            'symbol': symbol,
            'asset_volume': asset_volume,
            'trigger': trigger,
            'entry_point': entry_point,
            'stop_loss': stop,
            'take_profit': take_profit
        }
        # Write the opened order to the table
        # and send a message about opening a position.
        Manager.add_to_table(OpenedOrderDB, open_order_params)
        text_message: str = (
            InfoMessage.OPEN_ORDER_MESSAGE
            .format(**open_order_params)
        )
        send_message(text_message)

    @staticmethod
    def get_wallet_balance() -> dict[str, float]:
        """Request a wallet balance in USDT."""
        info: dict[str, Any] = session_http.get_wallet_balance(
            accountType=CONTRACT, coin=USDT
        )
        coin: str = info['result']['list'][0]['coin'][0]
        equity: float = round(
            float(coin['equity']), 2
        )
        unreal_pnl: float = round(
            float(coin['unrealisedPnl']), 2
        )
        balance: float = round(
            float(coin['walletBalance']), 2
        )
        real_pnl: float = round(
            float(coin['cumRealisedPnl']), 2
        )
        info_wallet: dict[str, float] = {
            'equity': equity,
            'unreal_pnl': unreal_pnl,
            'balance': balance,
            'real_pnl': real_pnl
        }
        return info_wallet

    @staticmethod
    def get_open_orders(ticker: str) -> list[dict[str, str]] | None:
        """Request for open orders."""
        symbol: str = f'{ticker}{USDT}'
        info: dict[str, Any] = session_http.get_open_orders(
            symbol=symbol, category=LINEAR
        )
        orders: list[dict[str, Any]] = info['result']['list']
        orders_list: list[dict[str, str]] = []
        if orders == orders_list:
            return None
        return orders

    @staticmethod
    def get_open_positions(ticker: str) -> list[dict[str, str]] | None:
        """Request for open positions."""
        symbol: str = f'{ticker}{USDT}'
        info = session_http.get_positions(symbol=symbol, category=LINEAR)
        positions: list[dict[str, Any]] = info['result']['list']
        if positions[0]['side'] == 'None':
            return None
        return positions

    @staticmethod
    def set_trailing_stop(
        symbol: str, trailing_stop: str, active_price: str
    ) -> None:
        try:
            session_http.set_trading_stop(
                symbol=symbol,
                category=LINEAR,
                trailingStop=trailing_stop,
                activePrice=active_price,
                positionIdx=0
            )
        except InvalidRequestError as error:
            send_message(error)
