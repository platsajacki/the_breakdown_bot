import logging as log

from requests import post

from settings import MYID, TOKEN
from exceptions import TelegramMessageError


def send_message(text_message: str | Exception) -> None:
    """Send a message in a telegram."""
    try:
        post(f'https://api.telegram.org/bot{TOKEN}/sendmessage?chat_id={MYID}&text={text_message}')  # noqa: E231
    except TelegramMessageError as error:
        log.error(error)
