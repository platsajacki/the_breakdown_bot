import logging as log
from functools import wraps

from bot_modules.send_message import send_message
from database.database import Session


def database_transaction(func):
    """The decorator for wrap a function into a database transaction."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        sess_db: Session = Session()
        try:
            sess_db.begin()
            func(sess_db, *args, **kwargs)
            sess_db.commit()
        except Exception as error:
            sess_db.rollback()
            log.error(error)
            send_message(error)
        finally:
            sess_db.close()
    return wrapper


def database_return(func):
    """
    The decorator for wrap a function into a database
    transaction with a result return.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        sess_db: Session = Session()
        try:
            sess_db.begin()
            result = func(sess_db, *args, **kwargs)
            sess_db.commit()
            return result
        except Exception as error:
            sess_db.rollback()
            log.error(error)
            send_message(error)
        finally:
            sess_db.close()
    return wrapper
