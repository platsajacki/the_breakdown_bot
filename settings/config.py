import os
from logging import Filter, LogRecord

from dotenv import load_dotenv

load_dotenv()


def get_required_env_var(var_name: str) -> str:
    """Get the value of a required environment variable."""
    if (value := os.getenv(var_name)) is None:
        raise ValueError(f'Environment variable `{var_name}` is not set. Please add it to your `.env` file.')
    return value


DEBUG = get_required_env_var('DEBUG') == 'True'

# API.
API_KEY = get_required_env_var('API_KEY')
API_SECRET = get_required_env_var('API_SECRET')
NOT_TESTNET = get_required_env_var('NOT_TESTNET') != 'True'
ACCOUNT_TYPE = get_required_env_var('ACCOUNT_TYPE')
CUSTOM_PING_INTERVAL: int = 15
CUSTOM_PING_TIMEOUT: int = 10


# Telegram token.
TOKEN = get_required_env_var('TOKEN')


# Admin ID.
MYID = int(get_required_env_var('MYID'))


# Access to the database.
POSTGRES_DB = get_required_env_var('POSTGRES_DB')
POSTGRES_LOGIN = get_required_env_var('POSTGRES_LOGIN')
POSTGRES_PASSWORD = get_required_env_var('POSTGRES_PASSWORD')
HOST = get_required_env_var('HOST')
ASYNC_DB_URL = f'postgresql+asyncpg://{POSTGRES_LOGIN}:{POSTGRES_PASSWORD}@{HOST}/{POSTGRES_DB}'  # noqa: E231

# Logging_config.
LOGS_DIR = 'logs'

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)


class ExcludeFilter(Filter):
    def filter(self, record: LogRecord):
        """Exclude messages with the text `ping/pong timed out`"""
        return "ping/pong timed out" not in record.getMessage()


LOG_CONFIG = {
    'version': 1,
    'root': {
        'handlers': ['fileHandler'],
        'level': 'WARNING',
    },
    'filters': {'ping_pong_filter': {'()': 'settings.config.ExcludeFilter'}},
    'handlers': {
        'fileHandler': {
            'class': 'logging.FileHandler',
            'filename': f'/{LOGS_DIR}/logfile.log',
            'level': 'WARNING',
            'formatter': 'fileFormatter',
            'filters': ['ping_pong_filter'],
        },
    },
    'formatters': {
        'fileFormatter': {
            'format': '\n%(name)s: %(asctime)s [%(levelname)s]\n%(funcName)s : %(lineno)d\nLog: %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S',
        },
    },
}
