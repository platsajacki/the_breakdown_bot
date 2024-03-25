import logging

from pybit.unified_trading import HTTP, WebSocket

from settings.config import API_KEY, API_SECRET, CUSTOM_PING_INTERVAL, CUSTOM_PING_TIMEOUT, NOT_TESTNET
from settings.constants import LINEAR
from tg_bot.send_message import log_and_send_error

logger = logging.getLogger(__name__)


async def get_ws_session_privat() -> WebSocket:
    """Setup a connection WebSocket."""
    try:
        ws_session_privat = WebSocket(
            testnet=NOT_TESTNET, api_key=API_KEY, api_secret=API_SECRET, channel_type='private'
        )
        ws_session_privat.ping_interval = CUSTOM_PING_INTERVAL
        ws_session_privat.ping_timeout = CUSTOM_PING_TIMEOUT
        return ws_session_privat
    except Exception as error:
        await log_and_send_error(logger, error, '`WebSocket session_privat`')


async def get_ws_session_public() -> WebSocket:
    """Setup a connection WebSocket."""
    try:
        ws_session_public = WebSocket(testnet=NOT_TESTNET, channel_type=LINEAR)
        ws_session_public.ping_interval = CUSTOM_PING_INTERVAL
        ws_session_public.ping_timeout = CUSTOM_PING_TIMEOUT
        return ws_session_public
    except Exception as error:
        await log_and_send_error(logger, error, 'WebSocket `session_public`')


async def get_session_http() -> HTTP:
    """Setup a connection with the exchange."""
    try:
        return HTTP(testnet=NOT_TESTNET, api_key=API_KEY, api_secret=API_SECRET)
    except Exception as error:
        await log_and_send_error(logger, error, '`session_http`')
