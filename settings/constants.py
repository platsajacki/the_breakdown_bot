from decimal import Decimal
from pathlib import Path

from emoji import emojize

from settings.config import get_required_env_var

BASE_DIR = Path(__file__).resolve().parent.parent

# Trading constants.
LINEAR = 'linear'

LONG = 'long'
SHORT = 'short'
TRENDS = [LONG, SHORT]
MIN_TURNOVER = Decimal(get_required_env_var('MIN_TURNOVER'))

BUY = 'Buy'
SELL = 'Sell'

MEDIAN_DAYS = 10
POWER_RESERVE_USED_UP = Decimal('0.333')
COEF_LEVEL_LONG = Decimal('0.998')
COEF_LEVEL_SHORT = Decimal('1.002')
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
MINUTE_IN_MILLISECONDS = 60000
