from aiogram import Bot, Dispatcher, executor, types
from keys import token

bot = Bot(token)
dp = Dispatcher(bot)

position = 'Long'


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Helo')


@dp.message_handler(commands=['Long'])
async def Long(message: types.Message):
    await message.answer('Включена торговля в Long')


@dp.message_handler(commands=['Short'])
async def Short(message: types.Message):
    await message.answer('Включена торговля в Short')

executor.start_polling(dp)
