from aiogram import Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from emoji import emojize

from ..filters import AdminID
from .bot_button import kb, kb_database
from .commands_main import check_and_get_value
from database.manager import Manager
from database.temporary_data.temp_db import DBState
from keys import MYID
from trade.check_price import connected_tickers


async def get_database(message: Message):
    await message.answer(
        'Choose next step:',
        reply_markup=kb_database
    )


async def chenge_stop(message: Message, state: FSMContext):
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


def reg_handler_db(dp: Dispatcher):
    dp.message.register(get_database, Command('database'), AdminID(MYID))
    dp.message.register(chenge_stop, Command('change_stop'), AdminID(MYID))
    dp.message.register(add_stop_volume, StateFilter(DBState.stop_volume))
    dp.message.register(
        get_connected_tickers, Command('connected_tickers'), AdminID(MYID)
    )
