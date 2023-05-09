import asyncio
import check_price
import tg_bot


async def coro_check_price():
    await asyncio.to_thread(check_price)
    await asyncio.sleep(1)


async def main():
    asyncio.gather(tg_bot, coro_check_price())


if __name__ == '__main__':
    asyncio.run(main())
