from time import time

import pytest

from settings.constants import LINEAR
from tests.factory import FixtureFactory


@pytest.fixture
def trade_data(factory: FixtureFactory) -> dict:
    schema = factory.schema(
        schema=lambda: {
            'category': LINEAR,
            'execTime': int(time() * 1000),
            'symbol': factory.symbol,
            'closedSize': 0,
            'side': factory.field('choice', items=['Buy', 'Sell']),
            'avgPrice': str(factory.price),
            'execQty': None,
            'execPrice': None,
        },
        iterations=1,
    )
    return {'data': schema.create()}


@pytest.fixture
def trade_position_data(factory: FixtureFactory) -> list[dict]:
    schema = factory.schema(
        schema=lambda: {
            'avgPrice': str(factory.price),
            'trailingStop': 0,
            'symbol': None,
            'size': 1,
            'side': None,
            'leverage': None,
            'markPrice': None,
            'unrealisedPnl': None,
            'stopLoss': None,
            'takeProfit': None,
        },
        iterations=1,
    )
    return schema.create()
