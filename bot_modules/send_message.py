from requests import post

from constant import MYID, TOKEN


def send_message(text_message):
    url = (f'https://api.telegram.org/bot{TOKEN}/sendmessage?'
           f'chat_id={MYID}&text={text_message}')
    post(url)
