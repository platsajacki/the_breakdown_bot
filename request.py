from pybit.unified_trading import HTTP
from keys import api_key, api_secret
import example

session = HTTP(
    testnet=True,
    api_key=api_key,
    api_secret=api_secret)


def check_level():
    if example.trend == 'Long':
        for symbol, levels in example.long_levels.items():
            info = session.get_tickers(category="linear", symbol=symbol)
            mark_price = float(info['result']['list'][0]['markPrice'])
            new_levels = []
            for level in levels:
                if level > mark_price:
                    new_levels.append(level)
            example.long_levels[symbol] = new_levels
    if example.trend == 'Short':
        print(example.short_levels)
        for symbol, levels in example.short_levels.items():
            info = session.get_tickers(category="linear", symbol=symbol)
            mark_price = float(info['result']['list'][0]['markPrice'])
            new_levels = []
            for level in levels:
                if level < mark_price:
                    new_levels.append(level)
            example.short_levels[symbol] = new_levels


def open_pos(symbol: str, entry_point: float, stop: float,
             take_profit: float, trigger: float, side: str):
    '''Calculation of transaction volume'''
    min_order_qty: str = session.get_instruments_info(
        category="linear",
        symbol=symbol)['result']['list'][0]['lotSizeFilter']['minOrderQty']
    round_volume: int = len(min_order_qty.split('.')[1])
    asset_volume: str = str(round((example.stop_volume
                                   / abs(entry_point - stop)),
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


def get_wallet_balance():
    return session.get_wallet_balance(accountType='UNIFIED', coin='USDT')


def get_open_orders():
    return session.get_open_orders(symbol='BTC', category='inverse',
                                   openOnly=1)
