from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage

from settings import TOKEN

# Build the bot.
bot: Bot = Bot(TOKEN)
dp: Dispatcher = Dispatcher(storage=MemoryStorage())
router: Router = Router()


def register_commands(router: Router, *commands: tuple) -> None:
    """Register multiple commands with the given router."""
    for command in commands:
        router.message.register(*command)
