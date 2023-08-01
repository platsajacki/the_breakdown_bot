from aiogram.filters.state import State, StatesGroup


class TickerState(StatesGroup):
    ticker_order: State = State()
    ticker_position: State = State()


class DBState(StatesGroup):
    ticker: State = State()
    lvl_db: State = State()
    trend: State = State()
    stop_volume: State = State()


class DBQuery(StatesGroup):
    ticker: State = State()
    limit: State = State()
    trend: State = State()
