import logging
from functools import wraps
from logging import config

from database.db import SQLSession
from settings import LOG_CONFIG

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
            logger.error(str(error), exc_info=True)
        finally:
            sess_db.close()
    return wrapper
