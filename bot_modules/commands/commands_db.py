from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from emoji import emojize

from ..filters import AdminID
from ..text_message import InfoMessage
from .bot_button import kb, kb_database, kb_query, kb_long_short
from .commands_main import check_and_get_value
from database.models import TickerDB, SpentLevelsDB, UnsuitableLevelsDB
from database.manager import Manager
from database.temporary_data.temp_db import DBState, DBQuery
from keys import MYID
from trade.check_price import connected_tickers
from trade.bot_request import Market


async def get_database(message: Message):
    await message.answer(
        'Choose next step.',
        reply_markup=kb_database
    )


async def change_stop(message: Message, state: FSMContext):
    await message.answer('Enter the stop volume:')
    await state.set_state(DBState.stop_volume)


async def add_stop_volume(message: Message, state: FSMContext):
    try:
        volume = check_and_get_value(message)
        Manager.changing_stop(volume)
        await state.clear()
        await message.answer(
            'The stop volume has been changed! '
            f'{emojize(":check_mark_button:")}',
            reply_markup=kb
        )
    except ValueError:
        await message.answer(
            'The value entered is incorrect! Try again:'
        )


async def get_connected_tickers(message: Message):
    await message.answer(f'''Connected tickers:
    {connected_tickers}''')


async def get_query(message: Message):
    await message.answer(
        'What request should be sent?', reply_markup=kb_query
    )


async def get_active_lvls(message: Message, state: FSMContext):
    await message.answer('Enter the ticker:')
    await state.update_data(table=TickerDB)
    await state.set_state(DBQuery.ticker)


async def get_spend_lvls(message: Message, state: FSMContext):
    await message.answer('Enter the ticker:')
    await state.update_data(table=SpentLevelsDB)
    await state.set_state(DBQuery.ticker)


async def get_unsuiteble_lvls(message: Message, state: FSMContext):
    await message.answer('Enter the ticker:')
    await state.update_data(table=UnsuitableLevelsDB)
    await state.set_state(DBQuery.ticker)


async def get_limit_lvls(message: Message, state: FSMContext):
    ticker = message.text.upper()
    if Market.get_symbol(ticker) == 'OK':
        await state.update_data(ticker=ticker)
        await message.answer('Enter the limit:')
        await state.set_state(DBQuery.limit)
    else:
        await message.answer('Ticker not found, try again:')
        await state.clear()
        await state.set_state(DBQuery.ticker)


async def get_query_trend(message: Message, state: FSMContext):
    try:
        limit = int(message.text)
        await state.update_data(limit=limit)
        await message.answer(
            'Enter the trend:',
            reply_markup=kb_long_short
        )
        await state.set_state(DBQuery.trend)
    except ValueError:
        await message.answer(
            'The value entered is incorrect! Try again:'
        )
        await state.clear()
        await state.set_state(DBQuery.limit)


async def get_queryset_lvl(message: Message, state: FSMContext):
    trend = message.text.lower()
    await state.update_data(trend=trend)
    data = await state.get_data()
    for query in Manager.get_limit_query(**data):
        query['create'] = query['create'].strftime('%H:%M %d.%m.%Y')
        await message.answer(InfoMessage.QUERY_LIMIT.format(**query))
    await message.answer(
        f'Done!{emojize(":check_mark_button:")}',
        reply_markup=kb
    )


def reg_handler_db(router: Router):
    router.message.register(get_database, Command('database'), AdminID(MYID))
    router.message.register(change_stop, Command('change_stop'), AdminID(MYID))
    router.message.register(add_stop_volume, StateFilter(DBState.stop_volume))
    router.message.register(
        get_connected_tickers, Command('connected_tickers'), AdminID(MYID)
    )
    router.message.register(get_query, Command('query'), AdminID(MYID))
    router.message.register(get_active_lvls, Command('active'), AdminID(MYID))
    router.message.register(get_spend_lvls, Command('spend'), AdminID(MYID))
    router.message.register(
        get_unsuiteble_lvls, Command('unsuiteble'), AdminID(MYID)
    )
    router.message.register(get_limit_lvls, StateFilter(DBQuery.ticker))
    router.message.register(get_query_trend, StateFilter(DBQuery.limit))
    router.message.register(get_queryset_lvl, StateFilter(DBQuery.trend))
