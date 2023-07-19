from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage

from constant import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
