from dataclasses import dataclass

from aiogram.filters import BaseFilter
from aiogram.types import Message

from settings.config import MYID


@dataclass
class AdminID(BaseFilter):
    """Set the admin ID."""
    MYID: int

    async def __call__(self, message: Message) -> bool:
        return bool(message.from_user and message.from_user.id == self.MYID)


admin_filter = AdminID(MYID)
