from aiogram.filters import BaseFilter
from aiogram.types import Message
from dataclasses import dataclass


@dataclass
class AdminID(BaseFilter):
    MYID: int

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == self.MYID
