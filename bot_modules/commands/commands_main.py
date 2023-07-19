from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from emoji import emojize

from ..filters import AdminID
from .bot_button import kb, kb_check_prices, kb_long_short
from constant import LONG, SHORT, TRENDS, MYID
from database.manager import Manager
from database.models import TickerDB
from database.temporary_data.temp_db import DBQuery, DBState
from trade.bot_request import Market
from trade.check_price import start_check_tickers
from trade.detector import LevelDetector


def check_and_get_value(message) -> float:
    value: str = message.text
    if ',' in value:
        value = value.replace(',', '.')
    value: float = float(value)
    return value


async def start_add_level(message: Message, state: FSMContext):
    await message.answer('Enter the ticker:')
    await state.set_state(DBState.ticker)


async def enter_level(message: Message, state: FSMContext):
    ticker = message.text.upper()
    if Market.get_symbol(ticker) == 'OK':
        await state.update_data(ticker=ticker)
        await message.answer('Enter the level:')
        await state.set_state(DBState.lvl_db)
    else:
        await message.answer('Ticker not found, try again:')
        await state.set_state(DBState.ticker)


async def enter_trend(message: Message, state: FSMContext):
    try:
        level = check_and_get_value(message)
        await state.update_data(level=level)
        await message.answer(
            'Enter the trend:',
            reply_markup=kb_long_short
        )
        await state.set_state(DBState.trend)
    except ValueError:
        await message.answer(
            'The value entered is incorrect! Try again:'
        )


async def add_level(message: Message, state: FSMContext):
    trend = message.text.lower()
    if trend in TRENDS:
        await state.update_data(trend=trend)
        data = await state.get_data()
    else:
        await message.answer(
            'The value entered is incorrect! Try again:'
        )
        await state.set_state(DBQuery.trend)
    if LevelDetector.check_level(**data):
        Manager.add_to_table(TickerDB, data)
        await message.answer(
            f'Level is added! {emojize(":check_mark_button:")}',
            reply_markup=kb
        )
    else:
        await message.answer(
            "The level doesn't meet the requirements!",
            reply_markup=kb
        )
    await state.clear()


async def check_prices(message: Message):
    await message.answer(
        'Choose the trend direction:',
        reply_markup=kb_check_prices
    )


async def start(message):
    await message.answer(
        'Analyzing the levels...'
    )
    await message.answer(
        emojize(':man_technologist:')
    )
    for row in Manager.get_all_rows(TickerDB):
        LevelDetector.check_levels(**row._asdict())
    await message.answer(
        f'Done! {emojize(":check_mark_button:")}'
    )
    await message.answer(
        f'Price check started! {emojize(":check_mark_button:")}'
    )
    start_check_tickers()


async def trade_long(message: Message):
    Manager.changing_trend(LONG)
    await message.answer(
        f'Long trading activated! {emojize(":check_mark_button:")}'
    )
    await message.answer(emojize(':chart_increasing:'),
                         reply_markup=kb)
    await start(message)


async def trade_short(message: Message):
    Manager.changing_trend(SHORT)
    await message.answer(
        f'Short trading activated! {emojize(":check_mark_button:")}'
    )
    await message.answer(
        emojize(':chart_decreasing:'),
        reply_markup=kb
    )
    await start(message)


def reg_handler_main(router: Router):
    router.message.register(
        check_prices, Command('check_prices'), AdminID(MYID)
    )
    router.message.register(
        start_add_level, Command('add_level'), AdminID(MYID)
    )
    router.message.register(enter_level, StateFilter(DBState.ticker))
    router.message.register(enter_trend, StateFilter(DBState.lvl_db))
    router.message.register(add_level, StateFilter(DBState.trend))
    router.message.register(trade_long, Command('trade_long'), AdminID(MYID))
    router.message.register(trade_short, Command('trade_short'), AdminID(MYID))
