import asyncio
from binance import AsyncClient
import keys


async def main():
    '''Initialise the client.'''
    client = await AsyncClient.create(keys.api_key,
                                      keys.api_secret,
                                      testnet=True)
    print(await client.futures_account())

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
