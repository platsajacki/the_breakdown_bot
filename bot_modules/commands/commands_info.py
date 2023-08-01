from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from emoji import emojize

from ..filters import AdminID
from ..text_message import InfoMessage
from .bot_button import kb, kb_info
from constants import MYID, SYMBOL_OK
from database.temporary_data.temp_db import TickerState
from trade.bot_request import Market


async def get_info(message: Message) -> None:
    await message.answer(
        'What information is needed?',
        reply_markup=kb_info
    )


async def get_balance(message: Message) -> None:
    await message.answer(
            InfoMessage.WALLET_MASSAGE.format(**Market.get_wallet_balance())
    )


async def get_orders(message: Message, state: FSMContext) -> None:
    await message.answer('Enter the ticker:')
    await state.set_state(TickerState.ticker_order)


async def get_ticker_order(message: Message, state: FSMContext) -> None:
    ticker: str = message.text.upper()
    if Market.get_symbol(ticker) == SYMBOL_OK:
        await message.answer(
            emojize(':man_technologist:')
        )
        open_orders: list[dict[str, str]] | None = (
            Market.get_open_orders(ticker)
        )
        if open_orders is None:
            await message.answer(
                'There are no open orders.'
            )
            await message.answer(
                emojize(':man_shrugging:'), reply_markup=kb
            )
        else:
            for order in open_orders:
                entry_point: float = float(order['entry_point'])
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
        await state.clear()
    else:
        await message.answer('Ticker not found, try again:')
        await state.set_state(TickerState.ticker_order)


async def get_positions(message: Message, state: FSMContext) -> None:
    await message.answer('Enter the ticker:')
    await state.set_state(TickerState.ticker_position)


async def get_ticker_position(message: Message, state: FSMContext) -> None:
    ticker: str = message.text.upper()
    if Market.get_symbol(ticker) == SYMBOL_OK:
        await message.answer(
            emojize(':man_technologist:')
        )
        open_positions: list[dict[str, str]] | None = (
            Market.get_open_positions(ticker)
        )
        if open_positions is None:
            await message.answer(
                'There are no open positions.'
            )
            await message.answer(
                emojize(':man_shrugging:'), reply_markup=kb
            )
        else:
            for position in open_positions:
                await message.answer(
                    InfoMessage.POSITION_MESSAGE.format(**position),
                    reply_markup=kb
                )
        await state.clear()
    else:
        await message.answer('Ticker not found, try again:')
        await state.set_state(TickerState.ticker_position)


async def get_back(message: Message) -> None:
    await message.answer('Main menu.', reply_markup=kb)


def reg_handler_info(router: Router) -> None:
    router.message.register(get_info, Command('info'), AdminID(MYID))
    router.message.register(get_balance, Command('balance'), AdminID(MYID))
    router.message.register(get_orders, Command('orders'), AdminID(MYID))
    router.message.register(get_back, Command('back'), AdminID(MYID))
    router.message.register(get_positions, Command('positions'), AdminID(MYID))
    router.message.register(
        get_ticker_position, StateFilter(TickerState.ticker_position)
    )
    router.message.register(
            get_ticker_order, StateFilter(TickerState.ticker_order)
    )
