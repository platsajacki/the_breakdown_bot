from decimal import Decimal

import pytest


@pytest.fixture
def level_data() -> dict:
    return {
        'ticker': 'BTC',
        'level': Decimal('50000.00'),
        'round_price': 2
    }
