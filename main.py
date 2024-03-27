import asyncio
import logging

from aiogram.filters import CommandStart
from aiogram.types import Message

import settings._logging_setup  # noqa: F401
import tg_bot.commands  # noqa: F401
from database.db import create_db
from database.managers import set_standart_stop
from settings.config import MYID
from settings.constants import FIRE, NO_ENTRY
from tg_bot.commands.buttons import kb
from tg_bot.create_bot import bot, dp, router
from tg_bot.send_message import log_and_send_error
from trade.check_positions import start_execution_stream

logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start(message: Message):
    """
    The "Start" command checks who started the work.
    If it is not an admin, then the client is not allowed.
    """
    if message.from_user and message.from_user.id == MYID:
        await message.answer(f'The Breakdown Bot activeted! {FIRE}', reply_markup=kb)
        return
    await message.answer(f'Access is denied! {NO_ENTRY}')


async def main():
    """Start trading-bot."""
    try:
        await create_db()
        await set_standart_stop()
        await asyncio.gather(dp.start_polling(bot), start_execution_stream())
    except Exception as error:
        await log_and_send_error(logger, error)


if __name__ in '__main__':
    asyncio.run(main())
