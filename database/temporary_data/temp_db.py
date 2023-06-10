from aiogram.filters.state import State, StatesGroup


class TickerState(StatesGroup):
    ticker_order = State()
    ticker_position = State()


class DBState(StatesGroup):
    ticker = State()
    lvl_db = State()
    trend = State()
    stop_volume = State()
