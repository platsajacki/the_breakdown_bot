from aiogram.filters import Command
from aiogram.types import Message
from emoji import emojize

from bot_modules.commands.bot_button import kb
from bot_modules.commands.commands_db import reg_handler_db
from bot_modules.commands.commands_info import reg_handler_info
from bot_modules.commands.commands_main import reg_handler_main
from bot_modules.create_bot import bot, dp, router
from constant import MYID

reg_handler_main(router)
reg_handler_info(router)
reg_handler_db(router)


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


if __name__ == '__main__':
    dp.include_router(router)
    dp.run_polling(bot)
