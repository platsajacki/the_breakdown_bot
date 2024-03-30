from asyncio import Lock
from decimal import Decimal
from typing import TypedDict

from sqlalchemy import Row


class PriceMovementTicker(TypedDict):
    price: Decimal
    time: int


class ConnectedTicker(TypedDict):
    lock: Lock
    row: Row | None
    active_task: bool
    price_movement: PriceMovementTicker
