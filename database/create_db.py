from database.db import engine
from database.managers import ConfigurationManager, RowManager
from database.models import Base, StopVolumeDB
from settings import STANDART_STOP
from tg_bot.send_message import send_message

# Create tables in the database defined in the metadata.
Base.metadata.create_all(engine)


async def set_standart_stop():
    """If the stop is not defined, then set the standard one."""
    if RowManager.get_row_by_id(StopVolumeDB, 1) is None:
        ConfigurationManager.change_stop(STANDART_STOP)
        await send_message(f'Added standard stop volume: {STANDART_STOP} USDT')
