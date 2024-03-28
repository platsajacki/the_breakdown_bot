from decimal import Decimal

from pytest_mock import MockerFixture, MockType

from settings.constants import LONG, SHORT
from trade.detector import LevelDetector


async def test_level_detector(mocker: MockerFixture, mock_market_get_mark_price: MockType):
    price = Decimal('100')
    mock_market_get_mark_price.return_value = price
    mocker.patch(
        'database.managers.TickerManager.get_levels_by_ticker_and_trend', return_value=[]
    )
    assert await LevelDetector.check_level('BTC', price + 1, LONG) is True
    assert await LevelDetector.check_level('BTC', price - 1, SHORT) is True
    assert await LevelDetector.check_level('BTC', price, LONG) is False
    assert await LevelDetector.check_level('BTC', price, SHORT) is False
