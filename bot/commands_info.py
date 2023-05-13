from aiogram import Dispatcher
from aiogram.types import Message
from .bot_button import kb, kb_info
from keys import MYID
from trade.request import get_wallet_balance, get_open_orders

ORDER_MESSAGE = '''Side - {side};
Entry point - {price};
Asset volume - {qty}:
Trigger - {trigger_price};
Stop-loss - {stop_loss};
Take-profit - {take_profit}.'''


async def get_info(message: Message):
    if message.from_user.id == MYID:
        await message.answer('What information is needed?',
                             reply_markup=kb_info)


async def get_balance(message: Message):
    if message.from_user.id == MYID:
        await message.answer(get_wallet_balance())


# Нужно добавить ввод симбвола и провекру их в базе
async def get_orders(message: Message):
    if message.from_user.id == MYID:
        for order in get_open_orders():
            await message.answer(ORDER_MESSAGE.format(**order))


async def get_back(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Main menu.', reply_markup=kb)


def reg_handler_info(dp: Dispatcher):
    dp.register_message_handler(get_info, commands=['info'])
    dp.register_message_handler(get_balance, commands=['balance'])
    dp.register_message_handler(get_orders, commands=['orders'])
    dp.register_message_handler(get_back, commands=['back'])
