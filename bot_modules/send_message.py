import logging as log
from requests import post

from exceptions import TelegramMessageError
from constants import MYID, TOKEN


def send_message(text_message: str) -> None:
    """Send a message in a telegram."""
    try:
        post(f'https://api.telegram.org/bot{TOKEN}/sendmessage?chat_id={MYID}&text={text_message}')
    except TelegramMessageError as error:
        log.error(error)
