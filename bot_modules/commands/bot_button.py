from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Keyboard
check_prices: KeyboardButton = KeyboardButton(text='/check_prices')
add_level: KeyboardButton = KeyboardButton(text='/add_level')
info_database: KeyboardButton = KeyboardButton(text='/info_database')

# Keyboard info
info_market: KeyboardButton = KeyboardButton(text='/info_market')
balance: KeyboardButton = KeyboardButton(text='/balance')
orders: KeyboardButton = KeyboardButton(text='/orders')
positions: KeyboardButton = KeyboardButton(text='/positions')
back: KeyboardButton = KeyboardButton(text='/back')

# Keyboard check_price
long_trend: KeyboardButton = KeyboardButton(text='/trade_long')
short_trend: KeyboardButton = KeyboardButton(text='/trade_short')

# Keyboard choise of a trend
long: KeyboardButton = KeyboardButton(text='long')
short: KeyboardButton = KeyboardButton(text='short')

# Keyboard db
change_stop: KeyboardButton = KeyboardButton(text='/change_stop')
connected_tickers: KeyboardButton = KeyboardButton(text='/connected_tickers')
query: KeyboardButton = KeyboardButton(text='/query')
active: KeyboardButton = KeyboardButton(text='/active')
spend: KeyboardButton = KeyboardButton(text='/spend')
unsuiteble: KeyboardButton = KeyboardButton(text='/unsuiteble')

# Add buttons
kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[add_level], [check_prices], [info_market], [info_database]], resize_keyboard=True
)
kb_info: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[balance], [orders], [positions], [back]], resize_keyboard=True
)
kb_check_prices: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[long_trend], [short_trend], [back]], resize_keyboard=True
)
kb_long_short: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[long, short]], resize_keyboard=True
)
kb_database: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[change_stop], [connected_tickers], [query], [back]], resize_keyboard=True
)
kb_query: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[active], [spend], [unsuiteble], [back]], resize_keyboard=True
)
