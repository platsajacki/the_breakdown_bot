from aiogram import Bot, Dispatcher, executor, types
from keys import token
from request import check_level

bot = Bot(token)
dp = Dispatcher(bot)

power = False


@dp.message_handler(commands=['check_level'])
async def start(message: types.Message):
    await message.answer('Анализирую уровни...')
    check_level()
    await message.answer('Готово!')


@dp.message_handler(commands=['c'])
async def c(message: types.Message):
    global power
    power = True


@dp.message_handler(commands=['Long'])
async def Long(message: types.Message):
    await message.answer('Включена торговля в Long')


@dp.message_handler(commands=['Short'])
async def Short(message: types.Message):
    await message.answer('Включена торговля в Short')

executor.start_polling(dp)
