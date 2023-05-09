from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from bot_button import kb, kb_info
from keys import token
from request import check_level  # get_wallet_balance, get_open_orders

bot = Bot(token)
dp = Dispatcher(bot)

power = False


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer('The Breakdown Bot activeted!',
                         reply_markup=kb)


@dp.message_handler(commands=['check_levels'])
async def check_levels(message: Message):
    await message.answer('Analyzing the levels...')
    check_level()
    await message.answer('Done!')


@dp.message_handler(commands=['check_prices'])
async def check_prices(message: Message):
    await message.answer('Price check started!')


@dp.message_handler(commands=['add_levels'])
async def add_levels(message: Message):
    await message.answer('Levels added!')


@dp.message_handler(commands=['long'])
async def trade_long(message: Message):
    await message.answer('Long trading activated!')


@dp.message_handler(commands=['short'])
async def trade_short(message: Message):
    await message.answer('Short trading activated!')


@dp.message_handler(commands=['info'])
async def get_info(message: Message):
    await message.answer('What information is needed?',
                         reply_markup=kb_info)


@dp.message_handler(commands=['balance'])
async def get_balance(message: Message):
    await message.answer('get_wallet_balance()')


@dp.message_handler(commands=['orders'])
async def get_orders(message: Message):
    await message.answer('get_open_orders()')

executor.start_polling(dp)
