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

'''Keyboard_check_price'''
yes_start_check = KeyboardButton('/yes_start_check')
no_get_back = KeyboardButton('/no_get_back')

kb_check_prices = ReplyKeyboardMarkup(resize_keyboard=True)

'''Add button'''
kb.add(add_levels).add(long, check_levels, short).add(check_prices)
kb.add(info)

kb_info.add(balance).add(orders).add(back)

kb_check_prices.add(yes_start_check).add(no_get_back)
