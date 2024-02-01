from decimal import Decimal

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.temporary_data import TickerState
from settings import MAN_SHRUGGING, MAN_TECHNOLOGIST, MYID, SYMBOL_OK
from tg_bot.commands.buttons import kb, kb_info
from tg_bot.filters import AdminID
from tg_bot.text_message import InfoMessage
from trade.requests import Market


async def get_info(message: Message) -> None:
    """Choose an information request."""
    await message.answer('What information is needed?', reply_markup=kb_info)


async def get_balance(message: Message) -> None:
    """Send a message with the wallet balance."""
    await message.answer(InfoMessage.WALLET_MASSAGE.format(**await Market.get_wallet_balance()))


async def get_orders(message: Message, state: FSMContext) -> None:
    """Request for open orders."""
    await message.answer('Enter the ticker:')
    await state.set_state(TickerState.ticker_order)


async def get_ticker_order(message: Message, state: FSMContext) -> None:
    """Select a ticker to request orders."""
    if message.text and (await Market.get_symbol(ticker := message.text.upper())) == SYMBOL_OK:
        await message.answer(MAN_TECHNOLOGIST)
        open_orders: list[dict[str, str]] | None = await Market.get_open_orders(ticker)
        if open_orders is None:
            await message.answer('There are no open orders.')
            await message.answer(MAN_SHRUGGING, reply_markup=kb)
        else:
            for order in open_orders:
                entry_point = Decimal(order['price'])
                if entry_point != 0:
                    await message.answer(InfoMessage.ORDER_MESSAGE.format(**order), reply_markup=kb)
                else:
                    await message.answer(InfoMessage.ORDER_TP_SL_MESSAGE.format(**order), reply_markup=kb)
        await state.clear()
    else:
        await message.answer('Ticker not found, try again:')
        await state.set_state(TickerState.ticker_order)


async def get_positions(message: Message, state: FSMContext) -> None:
    """Request for open positions."""
    await message.answer('Enter the ticker:')
    await state.set_state(TickerState.ticker_position)


async def get_ticker_position(message: Message, state: FSMContext) -> None:
    """Choose a ticker to request positions."""
    if message.text and Market.get_symbol(ticker := message.text.upper()) == SYMBOL_OK:
        await message.answer(MAN_TECHNOLOGIST)
        open_positions: list[dict[str, str]] | None = await Market.get_open_positions(ticker)
        if open_positions is None:
            await message.answer('There are no open positions.')
            await message.answer(MAN_SHRUGGING, reply_markup=kb)
        else:
            for position in open_positions:
                await message.answer(InfoMessage.POSITION_MESSAGE.format(**position), reply_markup=kb)
        await state.clear()
    else:
        await message.answer('Ticker not found, try again:')
        await state.set_state(TickerState.ticker_position)


async def get_back(message: Message) -> None:
    """Go back."""
    await message.answer('Main menu.', reply_markup=kb)


def get_handler_info() -> list[tuple]:
    """Get a list of handlers for info commands registration."""
    return [
        (get_info, Command('info_market'), AdminID(MYID)),
        (get_balance, Command('balance'), AdminID(MYID)),
        (get_orders, Command('orders'), AdminID(MYID)),
        (get_back, Command('back'), AdminID(MYID)),
        (get_positions, Command('positions'), AdminID(MYID)),
        (get_ticker_position, StateFilter(TickerState.ticker_position)),
        (get_ticker_order, StateFilter(TickerState.ticker_order)),
    ]
