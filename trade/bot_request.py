import requests
from pybit.unified_trading import HTTP
from keys import api_key, api_secret, token, MYID
from bot_modules.text_message import OPEN_ORDER_MESSAGE
import example

session = HTTP(
    testnet=True,
    api_key=api_key,
    api_secret=api_secret)


def get_symbol(symbol: str):
    url = ('https://api.bybit.com/'
           f'v5/market/tickers?category=linear&symbol={symbol}USDT')
    response = requests.get(url)
    return response.json()['retMsg']


# Надо оптимизировать
def check_level():
    if example.trend == 'Long':
        for symbol, levels in example.long_levels.items():
            info = session.get_tickers(category='linear', symbol=symbol)
            mark_price = float(info['result']['list'][0]['markPrice'])
            new_levels = []
            for level in levels:
                if level > mark_price:
                    new_levels.append(level)
            example.long_levels[symbol] = new_levels
    if example.trend == 'Short':
        print(example.short_levels)
        for symbol, levels in example.short_levels.items():
            info = session.get_tickers(category='linear', symbol=symbol)
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
        category='linear',
        symbol=symbol)['result']['list'][0]['priceFilter']['minPrice']
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
        category='linear',
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
    open_order_params = {'symbol': symbol,
                         'asset_volume': asset_volume,
                         'trigger': trigger,
                         'entry_point': entry_point,
                         'stop_loss': stop,
                         'take_profit': take_profit
                         }
    text_message = OPEN_ORDER_MESSAGE.format(**open_order_params)
    url = (f'https://api.telegram.org/bot{token}/sendmessage?'
           f'chat_id={MYID}&text={text_message}')
    requests.get(url)


def get_wallet_balance():
    info = session.get_wallet_balance(accountType='CONTRACT', coin='USDT')
    coin = info['result']['list'][0]['coin'][0]
    equity = round(float(coin['equity']), 2)
    unreal_pnl = round(float(coin['unrealisedPnl']), 2)
    balance = round(float(coin['walletBalance']), 2)
    real_pnl = round(float(coin['cumRealisedPnl']), 2)
    info_wallet = {'equity': equity,
                   'unreal_pnl': unreal_pnl,
                   'balance': balance,
                   'real_pnl': real_pnl}
    return info_wallet


def get_open_orders(ticket: str):
    symbol: str = ticket + 'USDT'
    info = session.get_open_orders(symbol=symbol, category='linear')
    orders = info['result']['list']
    orders_list = []
    if orders == []:
        return orders
    for order in orders:
        order_info = {'symbol': symbol,
                      'side': order['side'],
                      'entry_point': order['price'],
                      'qty': order['qty'],
                      'trigger_price': order['triggerPrice'],
                      'stop_loss': order['stopLoss'],
                      'take_profit': order['takeProfit'],
                      'order_type': order['orderType']
                      }
        orders_list.append(order_info)
    return orders_list


def get_open_positions(ticket: str):
    symbol: str = ticket + 'USDT'
    info = session.get_positions(symbol=symbol, category='linear')
    positions = info['result']['list']
    positions_list = []
    if positions[0]['side'] == 'None':
        return 'None'
    for position in positions:
        position_info = {'symbol': symbol,
                         'side': position['side'],
                         'size': position['size'],
                         'leverage': position['leverage'],
                         'avg_price': position['avgPrice'],
                         'unrealised_pnl': position['unrealisedPnl'],
                         'stop_loss': position['stopLoss'],
                         'take_profit': position['takeProfit']
                         }
        positions_list.append(position_info)
    return positions_list
