from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from emoji import emojize
from keys import MYID
from .bot_button import kb, kb_check_prices, kb_long_short
from database.models import TickerDB
from database.manager import Manager
from database.temporary_data.temp_db import DBState
from trade.check_price import start_check_tickers
from trade.bot_request import Market, LevelDetector


def check_and_get_value(message) -> float:
    value: str = message.text
    if ',' in value:
        value = value.replace(',', '.')
    value: float = float(value)
    return value


async def start_add_level(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Enter the ticker:')
        await DBState.ticker.set()


async def enter_level(message: Message, state: FSMContext):
    if message.from_user.id == MYID:
        ticker = message.text.upper()
        if Market.get_symbol(ticker) == 'OK':
            await state.update_data(ticker=ticker)
            await message.answer('Enter the level:')
            await DBState.lvl_db.set()
        else:
            await message.answer('Ticker not found, try again:')
            await state.finish()
            await DBState.ticker.set()


async def enter_trend(message: Message, state: FSMContext):
    if message.from_user.id == MYID:
        try:
            level = check_and_get_value(message)
            await state.update_data(level=level)
            await message.answer(
                'Enter the trend:',
                reply_markup=kb_long_short
            )
            await DBState.trend.set()
        except ValueError:
            await message.answer(
                'The value entered is incorrect! Try again:'
            )


async def add_level(message: Message, state: FSMContext):
    if message.from_user.id == MYID:
        trend = message.text.lower()
        await state.update_data(trend=trend)
        data = await state.get_data()
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
        await state.finish()


async def check_prices(message: Message):
    if message.from_user.id == MYID:
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
    if message.from_user.id == MYID:
        Manager.changing_trend('long')
        await message.answer(
            f'Long trading activated! {emojize(":check_mark_button:")}'
        )
        await message.answer(emojize(':chart_increasing:'),
                             reply_markup=kb)
        await start(message)


async def trade_short(message: Message):
    if message.from_user.id == MYID:
        Manager.changing_trend('short')
        await message.answer(
            f'Short trading activated! {emojize(":check_mark_button:")}'
        )
        await message.answer(
            emojize(':chart_decreasing:'),
            reply_markup=kb
        )
        await start(message)


def reg_handler_main(dp: Dispatcher):
    dp.register_message_handler(check_prices, commands=['check_prices'])
    dp.register_message_handler(start_add_level, commands=['add_level'])
    dp.register_message_handler(enter_level, state=DBState.ticker)
    dp.register_message_handler(enter_trend, state=DBState.lvl_db)
    dp.register_message_handler(add_level, state=DBState.trend)
    dp.register_message_handler(trade_long, commands=['long'])
    dp.register_message_handler(trade_short, commands=['short'])
