from aiogram.dispatcher.filters.state import StatesGroup, State


class Receipt(StatesGroup):
    hours_report = State()

