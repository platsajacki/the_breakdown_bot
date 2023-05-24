from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

'''Keyboard'''
check_prices = KeyboardButton('/check_prices')
add_level = KeyboardButton('/add_level')

kb = ReplyKeyboardMarkup(resize_keyboard=True)

'''Keyboard_info'''
info = KeyboardButton('/info')
balance = KeyboardButton('/balance')
orders = KeyboardButton('/orders')
positions = KeyboardButton('/positions')
back = KeyboardButton('/back')

kb_info = ReplyKeyboardMarkup(resize_keyboard=True)

'''Keyboard_check_price'''
long_trend = KeyboardButton('/long')
short_trend = KeyboardButton('/short')

kb_check_prices = ReplyKeyboardMarkup(resize_keyboard=True)

'''Keyboard choise of a trend'''
long = KeyboardButton(text='long')
short = KeyboardButton(text='short')

kb_long_short = ReplyKeyboardMarkup(resize_keyboard=True)

'''Add buttons'''
kb.add(add_level).add(check_prices).add(info)

kb_info.add(balance).add(orders).add(positions).add(back)

kb_check_prices.add(long_trend).add(short_trend)

kb_long_short.add(long, short)
