import logging
from logging import config

from aiogram.filters import CommandStart
from aiogram.types import Message

from settings import FIRE, LOG_CONFIG, MYID, NO_ENTRY
from tg_bot.commands import get_handler_db, get_handler_info, get_handler_main
from tg_bot.commands.buttons import kb
from tg_bot.create_bot import bot, dp, register_commands, router
from tg_bot.send_message import log_and_send_error
from trade.check_positions import start_execution

config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start(message: Message):
    """
    The "Start" command checks who started the work.
    If it is not an admin, then the client is not allowed.
    """
    if message.from_user and message.from_user.id == MYID:
        await message.answer(f'The Breakdown Bot activeted! {FIRE}', reply_markup=kb)
    else:
        await message.answer(f'Access is denied! {NO_ENTRY}')


def main():
    """Start trading-bot."""
    try:
        register_commands(router, *get_handler_db(), *get_handler_main(), *get_handler_info())
        start_execution()
        dp.include_router(router)
        dp.run_polling(bot)
    except Exception as error:
        log_and_send_error(logger, error)


if __name__ in '__main__':
    main()
