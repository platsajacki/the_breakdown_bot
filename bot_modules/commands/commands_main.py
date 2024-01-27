from typing import Any

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot_modules.commands.bot_button import kb, kb_check_prices, kb_long_short
from bot_modules.filters import AdminID
from constants import (
    CHART_DECREASING,
    CHART_INCREASING,
    CHECK_MARK_BUTTON,
    LONG,
    MAN_TECHNOLOGIST,
    MYID,
    SHORT,
    SYMBOL_OK,
    TRENDS,
)
from database.manager import Manager
from database.models import TickerDB
from database.temporary_data.temp_db import DBQuery, DBState
from trade.bot_request import Market
from trade.check_price import start_check_tickers
from trade.detector import LevelDetector


def check_and_get_value(message) -> float:
    """Conversion of the entered value to float."""
    value: str = message.text
    if ',' in value:
        value = value.replace(',', '.')
    value: float = float(value)
    return value


async def start_add_level(message: Message, state: FSMContext) -> None:
    """Start adding a new level."""
    await message.answer('Enter the ticker:')
    await state.set_state(DBState.ticker)


async def enter_level(message: Message, state: FSMContext) -> None:
    """Enter the price of the level."""
    if Market.get_symbol(ticker := message.text.upper()) == SYMBOL_OK:
        await state.update_data(ticker=ticker)
        await message.answer('Enter the level:')
        await state.set_state(DBState.lvl_db)
    else:
        await message.answer('Ticker not found, try again:')
        await state.set_state(DBState.ticker)


async def enter_trend(message: Message, state: FSMContext) -> None:
    """Enter a trend for the level"""
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


async def add_level(message: Message, state: FSMContext) -> None:
    """
    Check and add a level that meets the requirements.
    Or refusal to add.
    """
    trend: str = message.text.lower()
    if trend in TRENDS:
        await state.update_data(trend=trend)
        data: dict[str, Any] = await state.get_data()
    else:
        await message.answer(
            'The value entered is incorrect! Try again:'
        )
        await state.set_state(DBQuery.trend)
    if LevelDetector.check_level(**data):
        Manager.add_to_table(TickerDB, data)
        await message.answer(
            f'Level is added! {CHECK_MARK_BUTTON}',
            reply_markup=kb
        )
    else:
        await message.answer(
            "The level doesn't meet the requirements!",
            reply_markup=kb
        )
    await state.clear()


async def check_prices(message: Message) -> None:
    """Choose the direction of trade."""
    await message.answer(
        'Choose the trend direction:',
        reply_markup=kb_check_prices
    )


async def start(message) -> None:
    """Start the selection of checking levels by trend."""
    await message.answer(
        'Analyzing the levels...'
    )
    await message.answer(MAN_TECHNOLOGIST)
    for row in Manager.get_all_rows(TickerDB):
        LevelDetector.check_levels(**row)
    await message.answer(
        f'Done! {CHECK_MARK_BUTTON}'
    )
    await message.answer(
        f'Price check started! {CHECK_MARK_BUTTON}'
    )
    start_check_tickers()


async def trade_long(message: Message) -> None:
    """Change the trend to a long one."""
    Manager.changing_trend(LONG)
    await message.answer(
        f'Long trading activated! {CHECK_MARK_BUTTON}'
    )
    await message.answer(CHART_INCREASING, reply_markup=kb)
    await start(message)


async def trade_short(message: Message) -> None:
    """Change the trend to a short one."""
    Manager.changing_trend(SHORT)
    await message.answer(
        f'Short trading activated! {CHECK_MARK_BUTTON}'
    )
    await message.answer(CHART_DECREASING, reply_markup=kb)
    await start(message)


def reg_handler_main(router: Router) -> None:
    """Registration of main commands."""
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
