from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from emoji import emojize
from keys import MYID
from database.temporary_data.temp_db import Ticket
from trade.bot_request import (get_wallet_balance, get_open_orders, get_symbol,
                               get_open_positions)
from .bot_button import kb, kb_info
from .text_message import (ORDER_MESSAGE, ORDER_TP_SL_MESSAGE, WALLET_MASSAGE,
                           POSITION_MESSAGE)


async def get_info(message: Message):
    if message.from_user.id == MYID:
        await message.answer('What information is needed?',
                             reply_markup=kb_info)


async def get_balance(message: Message):
    if message.from_user.id == MYID:
        await message.answer(WALLET_MASSAGE.format(**get_wallet_balance()))


async def get_orders(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Enter the ticker:')
        await Ticket.ticket_order.set()


async def get_ticket_order(message: Message, state: FSMContext):
    tiker = message.text.upper()
    if message.from_user.id == MYID:
        await message.answer(emojize(':man_technologist:'))
        if get_symbol(tiker) == 'OK':
            open_orders = get_open_orders(tiker)
            if open_orders == []:
                await message.answer('There are no open orders.')
                await message.answer(emojize(':man_shrugging:'),
                                     reply_markup=kb)
                await state.finish()
            for order in open_orders:
                entry_point = float(order['entry_point'])
                if entry_point != 0:
                    await message.answer(ORDER_MESSAGE.format(**order),
                                         reply_markup=kb)
                else:
                    await message.answer(ORDER_TP_SL_MESSAGE.format(**order),
                                         reply_markup=kb)
            await state.finish()
        else:
            await message.answer('Ticker not found, try again:')
            await state.finish()
            await Ticket.ticket_order.set()


async def get_positions(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Enter the ticker:')
        await Ticket.ticket_position.set()


async def get_ticket_position(message: Message, state: FSMContext):
    tiker = message.text.upper()
    if message.from_user.id == MYID:
        await message.answer(emojize(':man_technologist:'))
        if get_symbol(tiker) == 'OK':
            open_positions = get_open_positions(tiker)
            if open_positions == 'None':
                await message.answer('There are no open positions.')
                await message.answer(emojize(':man_shrugging:'),
                                     reply_markup=kb)
                await state.finish()
            else:
                for position in open_positions:
                    await message.answer(POSITION_MESSAGE.format(**position),
                                         reply_markup=kb)
            await state.finish()
        else:
            await message.answer('Ticker not found, try again:')
            await state.finish()
            await Ticket.ticket_position.set()


async def get_back(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Main menu.', reply_markup=kb)


def reg_handler_info(dp: Dispatcher):
    dp.register_message_handler(get_info, commands=['info'])
    dp.register_message_handler(get_balance, commands=['balance'])
    dp.register_message_handler(get_orders, commands=['orders'])
    dp.register_message_handler(get_ticket_order, state=Ticket.ticket_order)
    dp.register_message_handler(get_positions, commands=['positions'])
    dp.register_message_handler(get_ticket_position,
                                state=Ticket.ticket_position)
    dp.register_message_handler(get_back, commands=['back'])
