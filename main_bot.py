from aiogram import executor
from aiogram.types import Message
from emoji import emojize
from keys import MYID
from bot_modules.create_bot import dp
from bot_modules.bot_button import kb
from bot_modules.commands_info import reg_handler_info
from bot_modules.commands_main import reg_handler_main
from bot_modules.commands_db import reg_handler_db

reg_handler_main(dp)
reg_handler_info(dp)
reg_handler_db(dp)


@dp.message_handler(commands=['start'])
async def start(message: Message):
    if message.from_user.id == MYID:
        await message.answer(
            f'The Breakdown Bot activeted! {emojize(":fire:")}',
            reply_markup=kb)
    else:
        await message.answer(f'Access is denied! {emojize(":no_entry:")}')


if __name__ == '__main__':
    executor.start_polling(dp)
