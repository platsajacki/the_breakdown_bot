from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Keyboard
check_prices = KeyboardButton(text='/check_prices')
add_levels = KeyboardButton(text='/add_levels')
info_database = KeyboardButton(text='/info_database')

# Keyboard levels
add_one_level = KeyboardButton(text='/add_one_level')
add_all_levels = KeyboardButton(text='/add_all_levels')

# Keyboard info
info_market = KeyboardButton(text='/info_market')
balance = KeyboardButton(text='/balance')
orders = KeyboardButton(text='/orders')
positions = KeyboardButton(text='/positions')
back = KeyboardButton(text='/back')

# Keyboard check_price
long_trend = KeyboardButton(text='/trade_long')
short_trend = KeyboardButton(text='/trade_short')

# Keyboard choise of a trend
long = KeyboardButton(text='long')
short = KeyboardButton(text='short')

# Keyboard db
change_stop = KeyboardButton(text='/change_stop')
connected_tickers = KeyboardButton(text='/connected_tickers')
query = KeyboardButton(text='/query')
active = KeyboardButton(text='/active')
spend = KeyboardButton(text='/spend')
unsuiteble = KeyboardButton(text='/unsuiteble')

# Add buttons
kb = ReplyKeyboardMarkup(
    keyboard=[[info_market], [info_database], [add_levels], [check_prices]], resize_keyboard=True
)
kb_levels = ReplyKeyboardMarkup(
    keyboard=[[add_one_level], [add_all_levels], [back]], resize_keyboard=True
)
kb_info = ReplyKeyboardMarkup(
    keyboard=[[balance], [orders], [positions], [back]], resize_keyboard=True
)
kb_check_prices = ReplyKeyboardMarkup(
    keyboard=[[long_trend], [short_trend], [back]], resize_keyboard=True
)
kb_long_short = ReplyKeyboardMarkup(
    keyboard=[[long, short]], resize_keyboard=True
)
kb_database = ReplyKeyboardMarkup(
    keyboard=[[change_stop], [connected_tickers], [query], [back]], resize_keyboard=True
)
kb_query = ReplyKeyboardMarkup(
    keyboard=[[active], [spend], [unsuiteble], [back]], resize_keyboard=True
)
