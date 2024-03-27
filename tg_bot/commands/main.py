import asyncio
from decimal import Decimal
from typing import Any

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.managers import ConfigurationManager, RowManager, TickerManager
from database.models import Ticker
from database.temporary_data import DBState
from settings.config import MYID
from settings.constants import (
    CHART_DECREASING,
    CHART_INCREASING,
    CHECK_MARK_BUTTON,
    LONG,
    MAN_TECHNOLOGIST,
    SHORT,
    SYMBOL_OK,
    TRENDS,
)
from tg_bot.commands.buttons import kb, kb_check_prices, kb_levels, kb_long_short
from tg_bot.create_bot import router
from tg_bot.filters import AdminID
from tg_bot.utils import check_and_get_value
from trade.check_price import start_check_tickers
from trade.define_levels import get_all_levels
from trade.detector import LevelDetector
from trade.requests import Market


@router.message(Command('add_levels'), AdminID(MYID))
async def start_add_levels(message: Message) -> None:
    await message.answer('One or all?', reply_markup=kb_levels)


@router.message(Command('add_all_levels'), AdminID(MYID))
async def add_all_levels(message: Message) -> None:
    await message.answer('There is a search for levels...')
    await message.answer(MAN_TECHNOLOGIST)
    levels = await get_all_levels()
    if levels:
        levels_objects = []
        for symbol, data in levels.items():
            ticker = symbol[:-4]
            db_levels = await TickerManager.get_levels_by_ticker(ticker)
            mark_price = await Market.get_mark_price(ticker)
            levels_counter = 0
            for level in data:
                level_decimal = Decimal(level)
                trend = LONG if level_decimal > mark_price else SHORT
                if level_decimal not in db_levels:
                    levels_objects.append(Ticker(ticker=ticker, level=level_decimal, trend=trend))
                    levels_counter += 1
            await message.answer(f'{levels_counter} levels have been found for the {ticker}.')
        await RowManager.add_all_rows(levels_objects)
        await message.answer(f'There are {len(levels_objects)} levels recorded in the database.')
        return
    await message.answer('An error occurred during the calculation of the levels.')


@router.message(Command('add_one_level'), AdminID(MYID))
async def start_add_one_level(message: Message, state: FSMContext) -> None:
    """Start adding a new level."""
    await message.answer('Enter the ticker:')
    await state.set_state(DBState.ticker)


@router.message(StateFilter(DBState.ticker))
async def enter_level(message: Message, state: FSMContext) -> None:
    """Enter the price of the level."""
    if message.text and (await Market.get_symbol(ticker := message.text.upper())) == SYMBOL_OK:
        await state.update_data(ticker=ticker)
        await message.answer('Enter the level:')
        await state.set_state(DBState.lvl_db)
    else:
        await message.answer('Ticker not found, try again:')
        await state.set_state(DBState.ticker)


@router.message(StateFilter(DBState.lvl_db))
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


@router.message(StateFilter(DBState.trend))
async def add_level(message: Message, state: FSMContext) -> None:
    """Check and add a level that meets the requirements. Or refusal to add."""
    if message.text and (trend := message.text.lower()) in TRENDS:
        await state.update_data(trend=trend)
        data: dict[str, Any] = await state.get_data()
    else:
        await message.answer(
            'The value entered is incorrect! Try again:'
        )
        await state.set_state(DBState.trend)
    if await LevelDetector.check_level(**data):
        await RowManager.add_row(Ticker, data)
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


@router.message(Command('check_prices'), AdminID(MYID))
async def check_prices(message: Message) -> None:
    """Choose the direction of trade."""
    await message.answer('Choose the trend direction:', reply_markup=kb_check_prices)


async def start(message) -> None:
    """Start the selection of checking levels by trend."""
    await message.answer(
        'Analyzing the levels...'
    )
    await message.answer(MAN_TECHNOLOGIST)
    tasks = []
    ticker = ''
    for row in await RowManager.get_all_rows(Ticker):
        if row['ticker'] != ticker:
            ticker = row['ticker']
            mark_price = await Market.get_mark_price(ticker)
        tasks.append(LevelDetector.check_levels(**row, mark_price=mark_price))
    await asyncio.gather(*tasks)
    await message.answer(
        f'Done! {CHECK_MARK_BUTTON}'
    )
    await message.answer(
        f'Price check started! {CHECK_MARK_BUTTON}'
    )
    await start_check_tickers()


@router.message(Command('trade_long'), AdminID(MYID))
async def trade_long(message: Message) -> None:
    """Change the trend to a long one."""
    await ConfigurationManager.change_trend(LONG)
    await message.answer(
        f'Long trading activated! {CHECK_MARK_BUTTON}'
    )
    await message.answer(CHART_INCREASING, reply_markup=kb)
    await start(message)


@router.message(Command('trade_short'), AdminID(MYID))
async def trade_short(message: Message) -> None:
    """Change the trend to a short one."""
    await ConfigurationManager.change_trend(SHORT)
    await message.answer(
        f'Short trading activated! {CHECK_MARK_BUTTON}'
    )
    await message.answer(CHART_DECREASING, reply_markup=kb)
    await start(message)
