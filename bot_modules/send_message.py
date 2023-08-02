import logging as log
from requests import post

from exceptions import TelegramMessageError
from constants import MYID, TOKEN


def send_message(text_message: str) -> None:
    try:
        url: str = (f'https://api.telegram.org/bot{TOKEN}/sendmessage?'
                    f'chat_id={MYID}&text={text_message}')
        post(url)
    except TelegramMessageError as error:
        log.error(error, exc_info=True)
