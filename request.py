from pybit.unified_trading import HTTP
from example import stop_volume
from keys import api_key, api_secret

session = HTTP(
    testnet=True,
    api_key=api_key,
    api_secret=api_secret)


def open_pos(symbol: str, entry_point: float, stop: float,
             take_profit: float, trigger: float, side: str):
    '''Calculation of transaction volume'''
    min_order_qty: str = session.get_instruments_info(
        category="linear",
        symbol=symbol)['result']['list'][0]['lotSizeFilter']['minOrderQty']
    round_volume: int = len(min_order_qty.split('.')[1])
    asset_volume: str = str(round((stop_volume / abs(entry_point - stop)),
                                  round_volume))
    '''Setting up a trigger'''
    if side == 'Buy':
        triggerDirection: int = 1
    else:
        triggerDirection: int = 2
    '''Opening an order'''
    session.place_order(
        category='inverse',
        symbol=symbol,
        side=side,
        orderType='Limit',
        qty=asset_volume,
        tryggeBy='MarkPrice',
        triggerDirection=triggerDirection,
        triggerPrice=str(trigger),
        price=str(entry_point),
        takeProfit=str(take_profit),
        stopLoss=str(stop),
        orderFilter='Order')
    print(f'''Выставлен ордер - {symbol};
Объем позиции - {asset_volume}
Триггер - {trigger};
ТВХ - {entry_point};
Стоп-лосс - {stop};
Тейк-профит - {take_profit}.'''
          )
