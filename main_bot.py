from aiogram import executor
from aiogram.types import Message
from emoji import emojize
from keys import MYID
from bot.create_bot import dp
from bot.bot_button import kb
from bot.commands_info import reg_handler_info
from bot.commands_main import reg_handler_main


reg_handler_main(dp)
reg_handler_info(dp)


@dp.message_handler(commands=['start'])
async def start(message: Message):
    if message.from_user.id == MYID:
        await message.answer('The Breakdown Bot activeted! '
                             + emojize(':fire:'), reply_markup=kb)
    else:
        await message.answer('Access is denied! ' + emojize(':no_entry:'))


if __name__ == '__main__':
    executor.start_polling(dp)
