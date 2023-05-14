from aiogram.dispatcher.filters.state import State, StatesGroup


class Ticket(StatesGroup):
    ticket_order = State()
    ticket_position = State()
    data_open = State()
