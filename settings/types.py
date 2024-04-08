from asyncio import Lock
from decimal import Decimal
from typing import TypedDict

from sqlalchemy import Row


class ActiveTask(TypedDict):
    handle_message_ticker: bool
    handle_message_kline: bool


class ConnectedTicker(TypedDict):
    lock: Lock
    row: Row | None
    active_task: ActiveTask
    price_movement: Decimal | None
