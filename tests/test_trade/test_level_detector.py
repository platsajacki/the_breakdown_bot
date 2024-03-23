import pytest
from decimal import Decimal

from pytest_mock import MockerFixture, MockType

from settings.constants import LONG, SHORT
from trade.detector import LevelDetector


async def test_level_detector(mocker: MockerFixture, mock_market_get_mark_price: MockType):
    price = Decimal('100')
    mock_market_get_mark_price.return_value = price
    mocker.patch(
        'database.managers.TickerManager.get_level_by_trend', return_value=[]
    )
    assert await LevelDetector.check_level('BTC', price + 1, LONG) is True
    assert await LevelDetector.check_level('BTC', price - 1, SHORT) is True
    assert await LevelDetector.check_level('BTC', price, LONG) is False
    assert await LevelDetector.check_level('BTC', price, SHORT) is False


@pytest.mark.parametrize(
    'trend, level, expected_call',
    [
        (LONG, Decimal('90.0'), 0),
        (LONG, Decimal('110.0'), 1),
        (SHORT, Decimal('90.0'), 1),
        (SHORT, Decimal('110.0'), 0),
    ]
)
async def test_check_levels(
    mocker: MockerFixture, mock_market_get_mark_price: MockType, trend: str, level: Decimal, expected_call: int
):
    mock_market_get_mark_price.return_value = Decimal('100')
    mock_transferring_row = mocker.patch('database.managers.RowManager.transferring_row')
    kwargs = {
        'ticker': 'BTC',
        'id': 1,
        'level': level,
        'trend': trend,
        'median_price': None,
        'update_median_price': None
    }
    await LevelDetector.check_levels(**kwargs)

    mock_transferring_row.call_count = expected_call
