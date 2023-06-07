from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from emoji import emojize
from keys import MYID
from .text_message import InfoMessage
from .bot_button import kb, kb_info
from database.temporary_data.temp_db import TickerState
from trade.bot_request import Market


async def get_info(message: Message):
    if message.from_user.id == MYID:
        await message.answer(
            'What information is needed?',
            reply_markup=kb_info
        )


async def get_balance(message: Message):
    if message.from_user.id == MYID:
        await message.answer(
            InfoMessage.WALLET_MASSAGE.format(**Market.get_wallet_balance())
        )


async def get_orders(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Enter the ticker:')
        await TickerState.ticker_order.set()


async def get_ticker_order(message: Message, state: FSMContext):
    ticker = message.text.upper()
    if message.from_user.id == MYID:
        await message.answer(
            emojize(':man_technologist:')
        )
        if Market.get_symbol(ticker) == 'OK':
            open_orders = Market.get_open_orders(ticker)
            if open_orders == []:
                await message.answer(
                    'There are no open orders.'
                )
                await message.answer(
                    emojize(':man_shrugging:'), reply_markup=kb
                )
                await state.finish()
            for order in open_orders:
                entry_point = float(order['entry_point'])
                if entry_point != 0:
                    await message.answer(
                        InfoMessage.ORDER_MESSAGE.format(**order),
                        reply_markup=kb
                    )
                else:
                    await message.answer(
                        InfoMessage.ORDER_TP_SL_MESSAGE.format(**order),
                        reply_markup=kb
                    )
            await state.finish()
        else:
            await message.answer('Ticker not found, try again:')
            await state.finish()
            await TickerState.ticker_order.set()


async def get_positions(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Enter the ticker:')
        await TickerState.ticker_position.set()


async def get_ticker_position(message: Message, state: FSMContext):
    tiker = message.text.upper()
    if message.from_user.id == MYID:
        await message.answer(
            emojize(':man_technologist:')
        )
        if Market.get_symbol(tiker) == 'OK':
            open_positions = Market.get_open_positions(tiker)
            if open_positions == 'None':
                await message.answer(
                    'There are no open positions.'
                )
                await message.answer(
                    emojize(':man_shrugging:'), reply_markup=kb
                )
                await state.finish()
            else:
                for position in open_positions:
                    await message.answer(
                        InfoMessage.POSITION_MESSAGE.format(**position),
                        reply_markup=kb
                    )
            await state.finish()
        else:
            await message.answer('Ticker not found, try again:')
            await state.finish()
            await TickerState.ticker_position.set()


async def get_back(message: Message):
    if message.from_user.id == MYID:
        await message.answer('Main menu.', reply_markup=kb)


def reg_handler_info(dp: Dispatcher):
    dp.register_message_handler(get_info, commands=['info'])
    dp.register_message_handler(get_balance, commands=['balance'])
    dp.register_message_handler(get_orders, commands=['orders'])
    dp.register_message_handler(get_back, commands=['back'])
    dp.register_message_handler(get_positions, commands=['positions'])
    dp.register_message_handler(
        get_ticker_position, state=TickerState.ticker_position
    )
    dp.register_message_handler(
            get_ticker_order, state=TickerState.ticker_order
    )
