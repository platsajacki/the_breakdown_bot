from decimal import Decimal
from typing import Any

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.managers import ConfigurationManager, RowManager
from database.models import SpentLevelsDB, TickerDB, UnsuitableLevelsDB
from database.temporary_data import DBQuery, DBState
from settings import CHECK_MARK_BUTTON, MYID, SYMBOL_OK, TRENDS
from tg_bot.commands.buttons import kb, kb_database, kb_long_short, kb_query
from tg_bot.filters import AdminID
from tg_bot.text_message import InfoMessage
from tg_bot.utils import check_and_get_value
from trade.check_price import connected_tickers
from trade.requests import Market


async def get_database(message: Message) -> None:
    """Select a database request."""
    await message.answer('Choose next step.', reply_markup=kb_database)


async def change_stop(message: Message, state: FSMContext) -> None:
    """Stop-loss price change."""
    await message.answer('Enter the stop volume:')
    await state.set_state(DBState.stop_volume)


async def add_stop_volume(message: Message, state: FSMContext) -> None:
    """Record of the updated stop."""
    try:
        volume: Decimal = check_and_get_value(message)
        ConfigurationManager.change_stop(volume)
        await message.answer(f'The stop volume has been changed! {CHECK_MARK_BUTTON}', reply_markup=kb)
    except ValueError:
        await message.answer('The value entered is incorrect! Try again:')
        await state.set_state(DBState.stop_volume)
    await state.clear()


async def get_connected_tickers(message: Message) -> None:
    """Request for connected tickers."""
    if connected_tickers == set():
        await message.answer('There are no tickers connected.')
    else:
        await message.answer(f'Connected tickers: {', '.join(connected_tickers)}. Total: {len(connected_tickers)}.')


async def get_query(message: Message) -> None:
    """Select a query from the database."""
    await message.answer('What request should be sent?', reply_markup=kb_query)


async def get_active_lvls(message: Message, state: FSMContext) -> None:
    """Request for active levels."""
    await message.answer('Enter the ticker:')
    await state.update_data(table=TickerDB)
    await state.set_state(DBQuery.ticker)


async def get_spend_lvls(message: Message, state: FSMContext) -> None:
    """Request for used levels."""
    await message.answer('Enter the ticker:')
    await state.update_data(table=SpentLevelsDB)
    await state.set_state(DBQuery.ticker)


async def get_unsuiteble_lvls(message: Message, state: FSMContext) -> None:
    """Request for unsuitable levels."""
    await message.answer('Enter the ticker:')
    await state.update_data(table=UnsuitableLevelsDB)
    await state.set_state(DBQuery.ticker)


async def get_limit_lvls(message: Message, state: FSMContext) -> None:
    """Select the number of requested levels."""
    if message.text and (await Market.get_symbol(ticker := message.text.upper())) == SYMBOL_OK:
        await state.update_data(ticker=ticker)
        await message.answer('Enter the limit:')
        await state.set_state(DBQuery.limit)
    else:
        await message.answer('Ticker not found, try again:')
        await state.set_state(DBQuery.ticker)


async def get_query_trend(message: Message, state: FSMContext) -> None:
    """Select of the query trend."""
    try:
        await state.update_data(limit=int(message.text))  # type: ignore[arg-type]
        await message.answer('Enter the trend:', reply_markup=kb_long_short)
        await state.set_state(DBQuery.trend)
    except ValueError:
        await message.answer('The value entered is incorrect! Try again:')
        await state.set_state(DBQuery.limit)


async def get_queryset_lvl(message: Message, state: FSMContext) -> None:
    """The output of the request is a message in a telegram."""
    if message.text and (trend := message.text.lower()) in TRENDS:
        await state.update_data(trend=trend)
        data: dict[str, Any] = await state.get_data()
        for query in RowManager.get_limit_row(**data):
            query['create'] = query['create'].strftime('%H:%M %d.%m.%Y')
            await message.answer(
                InfoMessage.QUERY_LIMIT.format(**query)
            )
        await message.answer(f'Done!{CHECK_MARK_BUTTON}', reply_markup=kb)
    else:
        await message.answer('The value entered is incorrect! Try again:')
        await state.set_state(DBQuery.trend)
    await state.clear()


def get_handler_db() -> list[tuple]:
    """Get a list of handlers for db commands registration."""
    return [
        (get_database, Command('info_database'), AdminID(MYID)),
        (change_stop, Command('change_stop'), AdminID(MYID)),
        (add_stop_volume, StateFilter(DBState.stop_volume)),
        (get_connected_tickers, Command('connected_tickers'), AdminID(MYID)),
        (get_query, Command('query'), AdminID(MYID)),
        (get_active_lvls, Command('active'), AdminID(MYID)),
        (get_spend_lvls, Command('spend'), AdminID(MYID)),
        (get_unsuiteble_lvls, Command('unsuiteble'), AdminID(MYID)),
        (get_limit_lvls, StateFilter(DBQuery.ticker)),
        (get_query_trend, StateFilter(DBQuery.limit)),
        (get_queryset_lvl, StateFilter(DBQuery.trend)),
    ]
