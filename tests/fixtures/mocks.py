from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def common_mocks_check_positions(mocker: MockerFixture, trade_position_data: list[dict]) -> tuple[AsyncMock, ...]:
    return (
        mocker.patch('trade.check_positions.send_message', new_callable=AsyncMock),
        mocker.patch(
            'trade.check_positions.Market.get_open_positions', new_callable=AsyncMock, return_value=trade_position_data
        ),
        mocker.patch('trade.check_positions.Market.set_trailing_stop', new_callable=AsyncMock)
    )
