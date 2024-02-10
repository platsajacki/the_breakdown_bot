from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage

from settings.config import TOKEN

# Build the bot.
bot: Bot = Bot(TOKEN, parse_mode='HTML')
dp: Dispatcher = Dispatcher(storage=MemoryStorage())
router: Router = Router()
dp.include_router(router)
