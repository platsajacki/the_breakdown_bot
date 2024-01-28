from os import getenv

from dotenv import load_dotenv
from emoji import emojize

load_dotenv()


def get_required_env_var(var_name: str) -> str:
    """Get the value of a required environment variable."""
    if (value := getenv(var_name)) is None:
        raise ValueError(f'Environment variable {var_name} is not set. Please add it to your `.env` file.')
    return value


# API.
API_KEY: str = get_required_env_var('API_KEY')
API_SECRET: str = get_required_env_var('API_SECRET')
CUSTOM_PING_INTERVAL: int = 10
CUSTOM_PING_TIMEOUT: int = 5

# Telegram token.
TOKEN: str = get_required_env_var('TOKEN')

# Admin ID.
MYID: int = int(get_required_env_var('MYID'))

# Access to the database.
DATABASE: str = get_required_env_var('DATABASE')
LOGIN: str = get_required_env_var('LOGIN')
PASSWORD: str = get_required_env_var('PASSWORD')
HOST: str = get_required_env_var('HOST')

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
