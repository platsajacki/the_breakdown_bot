from decimal import Decimal
from os import getenv

from dotenv import load_dotenv
from emoji import emojize

load_dotenv()


def get_required_env_var(var_name: str) -> str:
    """Get the value of a required environment variable."""
    if (value := getenv(var_name)) is None:
        raise ValueError(f'Environment variable `{var_name}` is not set. Please add it to your `.env` file.')
    return value


# API.
API_KEY: str = get_required_env_var('API_KEY')
API_SECRET: str = get_required_env_var('API_SECRET')
TESTNET: bool = get_required_env_var('TESTNET') == 'True'
CUSTOM_PING_INTERVAL: int = 10
CUSTOM_PING_TIMEOUT: int = 5


# Telegram token.
TOKEN: str = get_required_env_var('TOKEN')


# Admin ID.
MYID = int(get_required_env_var('MYID'))


# Access to the database.
DATABASE: str = get_required_env_var('DATABASE')
LOGIN: str = get_required_env_var('LOGIN')
PASSWORD: str = get_required_env_var('PASSWORD')
HOST: str = get_required_env_var('HOST')


# Logging_config.
LOG_CONFIG = {
    'version': 1,
    'root': {
        'handlers': ['fileHandler'],
        'level': 'WARNING',
    },
    'handlers': {
        'fileHandler': {
            'class': 'logging.FileHandler',
            'filename': 'logfile.log',
            'level': 'WARNING',
            'formatter': 'fileFormatter',
        },
    },
    'formatters': {
        'fileFormatter': {
            'format': '%(name)s: %(asctime)s [%(levelname)s] %(funcName)s : %(lineno)d \nLog: %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S',
        },
    },
}


# Trading constants.
LINEAR = 'linear'
CONTRACT = 'CONTRACT'

LONG = 'long'
SHORT = 'short'
TRENDS: list[str] = [LONG, SHORT]

BUY = 'Buy'
SELL = 'Sell'

COEF_LEVEL_LONG = Decimal('0.9975')
COEF_LEVEL_SHORT = Decimal('1.0025')
STANDART_STOP = Decimal('2.5')
USDT = 'USDT'
SYMBOL_OK = 'OK'


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
MINUTE_IN_MILLISECONDS = 6000
