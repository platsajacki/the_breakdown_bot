from requests import post

from constants import MYID, TOKEN


def send_message(text_message) -> None:
    url: str = (f'https://api.telegram.org/bot{TOKEN}/sendmessage?'
                f'chat_id={MYID}&text={text_message}')
    post(url)
