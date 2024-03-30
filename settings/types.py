from asyncio import Lock
from decimal import Decimal
from typing import TypedDict

from sqlalchemy import Row


class PriceMovementTicker(TypedDict):
    price: Decimal | None
    time: int | None


class ConnectedTicker(TypedDict, total=False):
    lock: Lock | None
    row: Row | None
    active_task: bool
    price_movement: PriceMovementTicker | dict
