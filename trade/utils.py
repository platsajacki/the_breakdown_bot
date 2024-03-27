from asyncio import AbstractEventLoop
from typing import Any, Callable


def handle_message_coro(msg: dict[str, Any], coro: Callable, running_loop: AbstractEventLoop) -> None:
    running_loop.create_task(coro(msg))
