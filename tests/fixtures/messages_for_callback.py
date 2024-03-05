from datetime import datetime

import pytest

from settings.constants import LINEAR, USDT
from tests.factory import FixtureFactory


@pytest.fixture
def trade_data(factory: FixtureFactory) -> dict:
    schema = factory.schema(
        schema=lambda: {
            'category': LINEAR,
            'execTime': int(datetime.now().timestamp() - 30),
            'symbol': factory.field('cryptocurrency_iso_code') + USDT,
            'closedSize': str(factory.field('random.randint', a=1, b=1000)),
            'side': factory.field('choice', items=['Buy', 'Sell']),
            'avgPrice': factory.price,
        },
        iterations=1,
    )
    return schema.create()[0]


@pytest.fixture
def trade_position_data(factory: FixtureFactory) -> dict:
    schema = factory.schema(
        schema=lambda: {
            'avgPrice': factory.price,
            'trailingStop': factory.price,
        },
        iterations=1,
    )
    return schema.create()[0]
