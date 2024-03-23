from unittest.mock import AsyncMock

from pytest_mock import MockerFixture

from settings.config import API_KEY, API_SECRET, NOT_TESTNET
from tests.factory import FixtureFactory
from trade.check_positions import get_ws_session_privat, handle_message


async def test_get_ws_session_privat(mocker: MockerFixture):
    mock_websocket = mocker.patch('trade.check_positions.WebSocket')
    mock_log_and_send_error = mocker.patch('trade.check_positions.log_and_send_error')
    await get_ws_session_privat()

    mock_log_and_send_error.assert_not_called()
    mock_websocket.assert_called_once_with(
        testnet=NOT_TESTNET, api_key=API_KEY, api_secret=API_SECRET, channel_type='private'
    )


async def test_handle_message_with_valid_data(
    trade_position_data: list[dict],
    factory: FixtureFactory,
    trade_data: dict,
    common_mocks_check_positions: tuple[AsyncMock, ...],
):
    trade_position_data[0]['trailingStop'] = str(factory.price)
    mock_send_message, mock_get_open_positions, mock_set_trailing_stop = common_mocks_check_positions
    mock_get_open_positions.return_value = trade_position_data
    await handle_message(trade_data)

    assert mock_send_message.call_count == 2
    mock_get_open_positions.assert_called_once_with(ticker=trade_data['data'][0]['symbol'][:-4])
    mock_set_trailing_stop.assert_not_called()


async def test_handle_message_with_valid_data_witout_traling_stop(
    trade_data: dict,
    common_mocks_check_positions: tuple[AsyncMock, ...],
):
    mock_send_message, mock_get_open_positions, mock_set_trailing_stop = common_mocks_check_positions
    await handle_message(trade_data)

    assert mock_send_message.call_count == 2
    mock_get_open_positions.assert_called_once_with(ticker=trade_data['data'][0]['symbol'][:-4])
    mock_set_trailing_stop.assert_called_once()


async def test_handle_message_with_valid_data_closed_positions(
    mocker: MockerFixture,
    trade_data: dict,
    common_mocks_check_positions: tuple[AsyncMock, ...],
):
    mock_send_message, mock_get_open_positions, mock_set_trailing_stop = common_mocks_check_positions
    mock_get_open_positions.return_value = None
    mocker.patch('time.time', return_value=trade_data['data'][0]['execTime'] / 1000 - 100)
    await handle_message(trade_data)

    assert mock_send_message.call_count == 1
    mock_get_open_positions.assert_called_once_with(ticker=trade_data['data'][0]['symbol'][:-4])
    mock_set_trailing_stop.assert_not_called()
