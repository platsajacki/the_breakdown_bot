from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_KEY: str = getenv('API_KEY')
API_SECRET: str = getenv('API_SECRET')

TOKEN: str = getenv('TOKEN')

MYID: int = int(getenv('MYID'))

DATABASE: str = getenv('DATABASE')
LOGIN: str = getenv('LOGIN')
PASSWORD: str = getenv('PASSWORD')
HOST: str = getenv('HOST')

LINEAR: str = 'linear'
CONTRACT: str = 'CONTRACT'

LONG: str = 'long'
SHORT: str = 'short'
TRENDS: list[str, str] = [LONG, SHORT]

BUY: str = 'Buy'
SELL: str = 'Sell'

COEF_LEVEL_LONG: float = 0.9975
COEF_LEVEL_SHORT: float = 1.0025

USDT: str = 'USDT'
SYMBOL_OK: str = 'OK'
