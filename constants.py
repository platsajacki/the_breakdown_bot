from os import getenv
from dotenv import load_dotenv

load_dotenv()

# API.
API_KEY: str = getenv('API_KEY')
API_SECRET: str = getenv('API_SECRET')
CUSTOM_PING_INTERVAL: int = 10
CUSTOM_PING_TIMEOUT: int = 5

# Telegram token.
TOKEN: str = getenv('TOKEN')

# Admin ID.
MYID: int = int(getenv('MYID'))

# Access to the database.
DATABASE: str = getenv('DATABASE')
LOGIN: str = getenv('LOGIN')
PASSWORD: str = getenv('PASSWORD')
HOST: str = getenv('HOST')

# Trading constants.
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
