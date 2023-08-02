from aiogram.filters.state import State, StatesGroup


class TickerState(StatesGroup):
    """FSM for information commands."""
    ticker_order: State = State()
    ticker_position: State = State()


class DBState(StatesGroup):
    """FSM for writing commands to tables."""
    ticker: State = State()
    lvl_db: State = State()
    trend: State = State()
    stop_volume: State = State()


class DBQuery(StatesGroup):
    """FSM for query commands."""
    ticker: State = State()
    limit: State = State()
    trend: State = State()
