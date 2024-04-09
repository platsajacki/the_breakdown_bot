from asyncio import Lock
from datetime import datetime
from decimal import Decimal
from typing import TypedDict

from sqlalchemy import Row


class ActiveTask(TypedDict):
    handle_message_ticker: bool
    handle_message_kline: bool


class ConnectedTicker(TypedDict):
    lock: Lock
    row: Row | None
    update_row: datetime
    active_task: ActiveTask
    price_movement: Decimal | None
