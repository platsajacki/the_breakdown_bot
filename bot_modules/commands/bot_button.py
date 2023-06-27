from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

'''Keyboard'''
check_prices = KeyboardButton(text='/check_prices')
add_level = KeyboardButton(text='/add_level')
database = KeyboardButton(text='/database')

'''Keyboard info'''
info = KeyboardButton(text='/info')
balance = KeyboardButton(text='/balance')
orders = KeyboardButton(text='/orders')
positions = KeyboardButton(text='/positions')
back = KeyboardButton(text='/back')

'''Keyboard check_price'''
long_trend = KeyboardButton(text='/trade_long')
short_trend = KeyboardButton(text='/trade_short')

'''Keyboard choise of a trend'''
long = KeyboardButton(text='long')
short = KeyboardButton(text='short')

'''Keyboard db'''
change_stop = KeyboardButton(text='/change_stop')
connected_tickers = KeyboardButton(text='/connected_tickers')

'''Add buttons'''
kb = ReplyKeyboardMarkup(
    keyboard=[
        [add_level], [check_prices], [info], [database]
    ],
    resize_keyboard=True
)

kb_info = ReplyKeyboardMarkup(
    keyboard=[
        [balance], [orders], [positions], [back]
    ], resize_keyboard=True
)

kb_check_prices = ReplyKeyboardMarkup(
    keyboard=[
        [long_trend], [short_trend], [back]
    ], resize_keyboard=True
)
kb_long_short = ReplyKeyboardMarkup(
    keyboard=[
        [long, short]
    ], resize_keyboard=True
)

kb_database = ReplyKeyboardMarkup(
    keyboard=[
        [change_stop], [connected_tickers], [back]
    ], resize_keyboard=True
)
