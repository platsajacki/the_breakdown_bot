from requests import post
from keys import token, MYID


def send_message(text_message):
    url = (f'https://api.telegram.org/bot{token}/sendmessage?'
           f'chat_id={MYID}&text={text_message}')
    post(url)
