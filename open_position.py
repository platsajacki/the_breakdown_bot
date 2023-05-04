from pybit.unified_trading import HTTP
import keys

session = HTTP(
    testnet=True,
    api_key=keys.api_key,
    api_secret=keys.api_secret)


def open_long(symbol, entry_point, stop, take_profit, trigger):
    print(symbol, entry_point, stop, take_profit, trigger)
    session.place_order(
        category='inverse',
        symbol=symbol,
        side='Buy',
        orderType='Limit',
        qty='0.05',
        tryggeBy='MarkPrice',
        triggerDirection=1,
        triggerPrice=str(trigger),
        price=str(entry_point),
        takeProfit=str(take_profit),
        stopLoss=str(stop),
        orderFilter='Order')


# session.place_order(
#         category='inverse',
#         symbol='ETHUSDT',
#         side='Buy',
#         orderType='Limit',
#         qty='0.05',
#         tryggeBy='MarkPrice',
#         triggerDirection=1,
#         triggerPrice='2000',
#         price='2010',
#         takeProfit='2200',
#         stopLoss='1999',
#         orderFilter='Order')
