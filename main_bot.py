from aiogram.filters import Command
from aiogram.types import Message
from emoji import emojize

import setup_log
from bot_modules.commands.bot_button import kb
from bot_modules.commands.commands_db import reg_handler_db
from bot_modules.commands.commands_info import reg_handler_info
from bot_modules.commands.commands_main import reg_handler_main
from bot_modules.create_bot import bot, dp, router
from bot_modules.send_message import send_message
from constants import MYID


@router.message(Command('start'))
async def start(message: Message):
    if message.from_user.id == MYID:
        await message.answer(
            f'The Breakdown Bot activeted! {emojize(":fire:")}',
            reply_markup=kb
        )
    else:
        await message.answer(
            f'Access is denied! {emojize(":no_entry:")}'
        )

reg_handler_main(router)
reg_handler_info(router)
reg_handler_db(router)

if __name__ == '__main__':
    try:
        dp.include_router(router)
        dp.run_polling(bot)
    except Exception as error:
        setup_log.log.error(error, exc_info=True)
        send_message(error)
