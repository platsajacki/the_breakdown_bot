from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

'''Keyboard'''
check_levels = KeyboardButton('/check_levels')
check_prices = KeyboardButton('/check_prices')
add_levels = KeyboardButton('/add_levels')
long = KeyboardButton('/long')
short = KeyboardButton('/short')

kb = ReplyKeyboardMarkup(resize_keyboard=True)

'''Keyboard_info'''
info = KeyboardButton('/info')
balance = KeyboardButton('/balance')
orders = KeyboardButton('/orders')
back = KeyboardButton('/back')

kb_info = ReplyKeyboardMarkup(resize_keyboard=True)

'''Add button'''
kb.add(check_levels).add(check_prices).add(add_levels)
kb.add(long, short).add(info)

kb_info.add(balance).add(orders).add(back)
