from aiogram.dispatcher.filters.state import StatesGroup, State


class Payment(StatesGroup):
    buy = State()
    top_up = State()
