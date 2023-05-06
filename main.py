import asyncio
import check_price


async def main():
    task_check_price = asyncio.to_thread(check_price)
    await asyncio.gather(task_check_price)


if __name__ == '__main__':
    asyncio.run(main())
