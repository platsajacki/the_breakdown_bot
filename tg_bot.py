from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from emoji import emojize
from bot_button import kb, kb_info
from keys import token, MYID
from request import check_level  # get_wallet_balance, get_open_orders

bot = Bot(token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: Message):
    if message.from_user.id == MYID:
        await message.answer('The Breakdown Bot activeted! '
                             + emojize(':fire:'), reply_markup=kb)
    else:
        await message.answer('Access is denied! ' + emojize(':no_entry:'))


@dp.message_handler(commands=['check_levels'])
async def check_levels(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Analyzing the levels...')
        check_level()
        await message.answer('Done!')


@dp.message_handler(commands=['check_prices'])
async def check_prices(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Price check started! '
                             + emojize(':chart_increasing_with_yen:'))


@dp.message_handler(commands=['add_levels'])
async def add_levels(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Levels added!')


@dp.message_handler(commands=['long'])
async def trade_long(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Long trading activated!')
        await message.answer(emojize(':chart_increasing:'))


@dp.message_handler(commands=['short'])
async def trade_short(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Short trading activated!')
        await message.answer(emojize(':chart_decreasing:'))


@dp.message_handler(commands=['info'])
async def get_info(message: Message):
    if message.from_user.id == MYID:
        await message.answer('What information is needed?',
                             reply_markup=kb_info)


@dp.message_handler(commands=['balance'])
async def get_balance(message: Message):
    if message.from_user.id == MYID:
        await message.answer('get_wallet_balance()')


@dp.message_handler(commands=['orders'])
async def get_orders(message: Message):
    if message.from_user.id == MYID:
        await message.answer('get_open_orders()')


@dp.message_handler(commands=['back'])
async def get_back(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Main menu.', reply_markup=kb)

executor.start_polling(dp)
