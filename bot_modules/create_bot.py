from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from keys import token

bot = Bot(token)
dp = Dispatcher(storage=MemoryStorage())
