from asyncio import AbstractEventLoop, Lock, Semaphore, sleep
from typing import Any, Callable

from database.temporary_data import CONNECTED_TICKERS

semaphore = Semaphore(10)


def handle_message_coro(
    msg: dict[str, Any], coro: Callable, running_loop: AbstractEventLoop, ticker: str | None = None
) -> None:
    async def lock_coro() -> None:
        if not ticker:
            await coro(msg)
            return
        lock = CONNECTED_TICKERS[ticker].setdefault('lock', Lock())
        if isinstance(lock, Lock):
            async with lock:
                await semaphore.acquire()
                await coro(msg)
                await sleep(3)
                semaphore.release()
    running_loop.create_task(lock_coro())
