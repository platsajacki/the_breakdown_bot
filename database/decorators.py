import asyncio
import logging
from functools import wraps

from database.db import SQLSession
from tg_bot.send_message import log_and_send_error

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
            asyncio.create_task(log_and_send_error(logger, error))
        finally:
            sess_db.close()
    return wrapper
