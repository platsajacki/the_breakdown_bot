from logging import DEBUG as LOGGING_DEBUG
from logging import basicConfig
from logging.config import dictConfig

from settings.config import DEBUG, LOG_CONFIG

if DEBUG:
    basicConfig(level=LOGGING_DEBUG)
else:
    dictConfig(LOG_CONFIG)
