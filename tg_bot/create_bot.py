from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage

from settings.config import TOKEN

# Build the bot.
bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)
