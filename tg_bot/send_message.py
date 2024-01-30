import logging
from logging import Logger, config

from requests import post

from settings import LOG_CONFIG, MYID, TOKEN

config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)


def send_message(text_message: str) -> None:
    """Send a message in a telegram."""
    try:
        post(f'https://api.telegram.org/bot{TOKEN}/sendmessage?chat_id={MYID}&text={text_message}')  # noqa: E231
    except Exception as e:
        logger.error(f'The message was not sent. Text: `{text_message}` {str(e)}.')


def log_and_send_error(logger: Logger, exception: Exception, error_message: str = 'bot') -> None:
    """Log details of an exception and send an error message."""
    msg = f'Error {error_message}: {str(exception)}'
    logger.error(msg, exc_info=True)
    send_message(msg)
