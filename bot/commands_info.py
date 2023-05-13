from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from emoji import emojize
from .bot_button import kb, kb_info
from keys import MYID
from database.temporary_data.temp_db import Ticker
from trade.request import (get_wallet_balance, get_open_orders, get_symbol)

ORDER_MESSAGE = '''{symbol}:
Side - {side};
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


# Добавить ввод тикета и формат его
async def get_orders(message: Message):
    await message.answer('Enter the ticker:')
    await Ticker.test.set()


async def get_ticket_order(message: Message, state: FSMContext):
    tiker = message.text
    if message.from_user.id == MYID:
        await message.answer(emojize(':man_technologist:'))
        if get_symbol(tiker) == 'OK':
            for order in get_open_orders(tiker):
                await message.answer(ORDER_MESSAGE.format(**order))
    # else:
    #     await message.answer('Ticker not found, enter again:')

# Добавить открытые позиции по тикету


async def get_back(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Main menu.', reply_markup=kb)


def reg_handler_info(dp: Dispatcher):
    dp.register_message_handler(get_info, commands=['info'])
    dp.register_message_handler(get_balance, commands=['balance'])
    dp.register_message_handler(get_orders, commands=['orders'])
    dp.register_message_handler(get_ticket_order, state=Ticker.test)
    dp.register_message_handler(get_back, commands=['back'])
