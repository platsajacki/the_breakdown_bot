from aiogram import Dispatcher
from aiogram.types import Message
from emoji import emojize
from .bot_button import kb, kb_check_prices
from keys import MYID
from trade.check_price import start_check_price
from trade.request import check_level


async def check_levels(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Analyzing the levels...')
        await message.answer(emojize(':man_technologist:'))
        check_level()
        await message.answer('Done!')


async def check_prices(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Are the levels checked? '
                             'Have you chosen a trade direction?',
                             reply_markup=kb_check_prices)


async def start_check(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Price check started! '
                             + emojize(':chart_increasing_with_yen:'),
                             reply_markup=kb)
        start_check_price()


async def no_get_back(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Main menu.', reply_markup=kb)


async def add_levels(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Levels added!')


async def trade_long(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Long trading activated!')
        await message.answer(emojize(':chart_increasing:'))


async def trade_short(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Short trading activated!')
        await message.answer(emojize(':chart_decreasing:'))


def reg_handler_main(dp: Dispatcher):
    dp.register_message_handler(check_levels, commands=['check_levels'])
    dp.register_message_handler(check_prices, commands=['check_prices'])
    dp.register_message_handler(start_check, commands=['yes_start_check'])
    dp.register_message_handler(no_get_back, commands=['no_get_back'])
    dp.register_message_handler(add_levels, commands=['add_levels'])
    dp.register_message_handler(trade_long, commands=['long'])
    dp.register_message_handler(trade_short, commands=['short'])
