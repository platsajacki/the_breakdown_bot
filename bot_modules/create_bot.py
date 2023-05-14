from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keys import token

bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())
