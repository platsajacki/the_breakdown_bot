from os import getenv

from dotenv import load_dotenv
from emoji import emojize

load_dotenv()

# API.
API_KEY: str | None = getenv('API_KEY')
API_SECRET: str | None = getenv('API_SECRET')
CUSTOM_PING_INTERVAL: int = 10
CUSTOM_PING_TIMEOUT: int = 5

# Telegram token.
TOKEN: str | None = getenv('TOKEN')

# Admin ID.
MYID: int = int(my_id) if (my_id := getenv('MYID')) else 0

# Access to the database.
DATABASE: str | None = getenv('DATABASE')
LOGIN: str | None = getenv('LOGIN')
PASSWORD: str | None = getenv('PASSWORD')
HOST: str | None = getenv('HOST')

# Trading constants.
LINEAR: str = 'linear'
CONTRACT: str = 'CONTRACT'

LONG: str = 'long'
SHORT: str = 'short'
TRENDS: list[str] = [LONG, SHORT]

BUY: str = 'Buy'
SELL: str = 'Sell'

COEF_LEVEL_LONG: float = 0.9975
COEF_LEVEL_SHORT: float = 1.0025

USDT: str = 'USDT'
SYMBOL_OK: str = 'OK'


# Smiles
ROCKET: str = emojize(':rocket:')
MONEY_WITH_WINGS: str = emojize(':money_with_wings:')
MONEY_BAG: str = emojize(':money_bag:')
CHECK_MARK_BUTTON: str = emojize(':check_mark_button:')
MAN_TECHNOLOGIST: str = emojize(':man_technologist:')
MAN_SHRUGGING: str = emojize(':man_shrugging:')
CHART_INCREASING: str = emojize(':chart_increasing:')
CHART_DECREASING: str = emojize(':chart_decreasing:')
FIRE: str = emojize(':fire:')
NO_ENTRY: str = emojize(':no_entry:')
COIN: str = emojize(':coin:')

# Time
MINUTE_IN_MILLISECONDS: int = 6000
