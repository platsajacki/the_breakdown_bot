import logging
from functools import wraps
from logging import config

from database.db import SQLSession
from settings import LOG_CONFIG
from tg_bot.send_message import log_and_send_error

config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)


def database_transaction(func):
    """The decorator for wrap a function into a database transaction."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        sess_db = SQLSession()
        try:
            sess_db.begin()
            result = func(sess_db, *args, **kwargs)
            sess_db.commit()
            return result
        except Exception as error:
            sess_db.rollback()
            log_and_send_error(logger, error, '`database_transaction`')
        finally:
            sess_db.close()
    return wrapper
