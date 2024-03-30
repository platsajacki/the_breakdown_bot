import asyncio
from asyncio import AbstractEventLoop, Lock, Semaphore, sleep
from typing import Any, Callable

from database.temporary_data import CONNECTED_TICKERS

semaphore = Semaphore(10)


async def lock_coro(msg: dict[str, Any], coro: Callable, ticker: str) -> None:
    """
    Handle messages from the exchange.
    Starts only if there is an asyncio.Lock for the ticker and if there are no tasks for the ticker.
    Lock is required to avoid resource contention for a single ticker.
    """
    lock = CONNECTED_TICKERS[ticker].get('lock')
    if isinstance(lock, Lock) and not CONNECTED_TICKERS[ticker].get('active_task'):
        print(CONNECTED_TICKERS[ticker]['active_task'])
        async with lock:
            await semaphore.acquire()
            CONNECTED_TICKERS[ticker]['active_task'] = True
            await asyncio.create_task(coro(msg))
            await sleep(3)
            CONNECTED_TICKERS[ticker]['active_task'] = False
            semaphore.release()


def handle_message_coro(
    msg: dict[str, Any], coro: Callable, running_loop: AbstractEventLoop, ticker: str | None = None
) -> None:
    """Run asynchronous handling of exchange messages."""
    if not ticker:
        running_loop.create_task(coro(msg))
        return
    running_loop.create_task(lock_coro(msg, coro, ticker))
