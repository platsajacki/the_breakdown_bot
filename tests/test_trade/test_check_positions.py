from unittest.mock import AsyncMock

from pytest_mock import MockerFixture

from settings.config import API_KEY, API_SECRET, TESTNET
from trade.check_positions import get_ws_session_privat


async def test_get_ws_session_privat(mocker: MockerFixture):
    mock_websocket = mocker.patch('trade.check_positions.WebSocket')
    mock_log_and_send_error = mocker.patch('trade.check_positions.log_and_send_error', new_callable=AsyncMock)
    await get_ws_session_privat()
    mock_log_and_send_error.assert_not_called()
    mock_websocket.assert_called_once_with(
        testnet=TESTNET, api_key=API_KEY, api_secret=API_SECRET, channel_type='private'
    )
