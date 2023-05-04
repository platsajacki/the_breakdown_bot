from pybit.unified_trading import HTTP
import keys

session = HTTP(
    testnet=True,
    api_key=keys.api_key,
    api_secret=keys.api_secret)


def open_pos(symbol, entry_point, stop, take_profit, trigger, side):
    if side == 'Buy':
        triggerDirection = 1
    else:
        triggerDirection = 2
    session.place_order(
        category='inverse',
        symbol=symbol,
        side=side,
        orderType='Limit',
        qty='0.05',
        tryggeBy='MarkPrice',
        triggerDirection=triggerDirection,
        triggerPrice=str(trigger),
        price=str(entry_point),
        takeProfit=str(take_profit),
        stopLoss=str(stop),
        orderFilter='Order')
    print(f'''Выставлен ордер - {symbol};
Триггер - {trigger};
ТВХ - {entry_point};
Стоп-лосс - {stop};
Тейк-профит - {take_profit}.'''
          )
