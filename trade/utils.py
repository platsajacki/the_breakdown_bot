import asyncio
from typing import Any, Coroutine


def handle_message_in_thread(msg: dict[str, Any], coro: Coroutine, main_loop: asyncio.AbstractEventLoop) -> None:
    """A message handler in a separate thread."""
    asyncio.set_event_loop(loop := asyncio.new_event_loop())
    try:
        loop.run_until_complete(coro(msg, main_loop))
    finally:
        loop.close()
