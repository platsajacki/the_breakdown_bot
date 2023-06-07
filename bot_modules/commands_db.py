from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from emoji import emojize
from keys import MYID
from .bot_button import kb, kb_database
from .commands_main import check_and_get_value
from database.manager import Manager
from database.temporary_data.temp_db import DBState


async def get_database(message: Message):
    if message.from_user.id == MYID:
        await message.answer(
            'Choose next step:',
            reply_markup=kb_database
        )


async def chenge_stop(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Enter the stop volume:')
        await DBState.stop_volume.set()


async def add_stop_volume(message: Message, state: FSMContext):
    if message.from_user.id == MYID:
        try:
            volume = check_and_get_value(message)
            Manager.changing_stop(volume)
            await state.finish()
            await message.answer(
                'The stop volume has been changed! '
                f'{emojize(":check_mark_button:")}',
                reply_markup=kb
            )
        except ValueError:
            await message.answer(
                'The value entered is incorrect! Try again:'
            )


def reg_handler_db(dp: Dispatcher):
    dp.register_message_handler(get_database, commands=['database'])
    dp.register_message_handler(chenge_stop, commands=['change_stop'])
    dp.register_message_handler(add_stop_volume, state=DBState.stop_volume)
