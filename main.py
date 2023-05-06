import asyncio
import check_price
import tg_bot


async def main():
    task_check_price = asyncio.to_thread(check_price)
    task_tg_bot = tg_bot
    await asyncio.gather(task_check_price, task_tg_bot)


if __name__ == '__main__':
    asyncio.run(main())
