import asyncio
from asyncio import AbstractEventLoop, Lock, Semaphore, sleep
from typing import Any, Callable

from database.temporary_data import CONNECTED_TICKERS

semaphore = Semaphore(10)


async def find_tasks_for_ticker(ticker: str):
    """Find running tasks for a ticker."""
    return list(
        filter(
            lambda task: task.get_name() == ticker,
            asyncio.all_tasks(),
        )
    )


async def lock_coro(msg: dict[str, Any], coro: Callable, ticker: str) -> None:
    """
    Handle messages from the exchange.
    Starts only if there is an asyncio.Lock for the ticker and if there are no tasks for the ticker.
    Lock is required to avoid resource contention for a single ticker.
    """
    lock = CONNECTED_TICKERS[ticker].setdefault('lock', Lock())
    if isinstance(lock, Lock) and not await find_tasks_for_ticker(ticker):
        async with lock:
            await semaphore.acquire()
            await asyncio.create_task(coro(msg), name=ticker)
            await sleep(3)
            semaphore.release()


def handle_message_coro(
    msg: dict[str, Any], coro: Callable, running_loop: AbstractEventLoop, ticker: str | None = None
) -> None:
    """Run asynchronous handling of exchange messages."""
    if not ticker:
        running_loop.create_task(coro(msg))
        return
    running_loop.create_task(lock_coro(msg, coro, ticker))
