from asyncio import Lock
from decimal import Decimal
from typing import TypedDict

from sqlalchemy import Row


class PriceMovementTicker(TypedDict):
    price: Decimal | None
    time: int | None


class ConnectedTicker(TypedDict):
    lock: Lock | None
    row: Row | None
    price_movement: PriceMovementTicker | dict
