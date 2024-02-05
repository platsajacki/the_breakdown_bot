import asyncio
import logging
from logging import Logger

from settings.config import MYID
from tg_bot.create_bot import bot

logger = logging.getLogger(__name__)


async def send_message(text_message: str, main_loop: None | asyncio.AbstractEventLoop = None) -> None:
    """Send a message in a telegram."""
    try:
        if main_loop:
            asyncio.run_coroutine_threadsafe(bot.send_message(MYID, text_message), main_loop)
            return
        await bot.send_message(MYID, text_message)
    except Exception as e:
        logger.error(f'The message was not sent. Text: `{text_message}` {str(e)}.', exc_info=True)


async def log_and_send_error(
    logger: Logger, exception: Exception, error_message: str = 'bot', main_loop: None | asyncio.AbstractEventLoop = None
) -> None:
    """Log details of an exception and send an error message."""
    msg = f'Error {error_message}: {str(exception)}'
    logger.error(msg, exc_info=True)
    await send_message(msg, main_loop)
