import os

from dotenv import load_dotenv

load_dotenv()


def get_required_env_var(var_name: str) -> str:
    """Get the value of a required environment variable."""
    if (value := os.getenv(var_name)) is None:
        raise ValueError(f'Environment variable `{var_name}` is not set. Please add it to your `.env` file.')
    return value


DEBUG: bool = get_required_env_var('DEBUG') == 'True'


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
POSTGRES_LOGIN: str = get_required_env_var('POSTGRES_LOGIN')
POSTGRES_PASSWORD: str = get_required_env_var('POSTGRES_PASSWORD')
HOST: str = get_required_env_var('HOST')


# Logging_config.
LOGS_DIR = 'logs'

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOG_CONFIG = {
    'version': 1,
    'root': {
        'handlers': ['fileHandler'],
        'level': 'WARNING',
    },
    'handlers': {
        'fileHandler': {
            'class': 'logging.FileHandler',
            'filename': f'/{LOGS_DIR}/logfile.log',
            'level': 'WARNING',
            'formatter': 'fileFormatter',
        },
    },
    'formatters': {
        'fileFormatter': {
            'format': '\n%(name)s: %(asctime)s [%(levelname)s]\n%(funcName)s : %(lineno)d\nLog: %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S',
        },
    },
}
