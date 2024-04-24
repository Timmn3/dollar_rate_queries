from aiogram.dispatcher.filters.state import StatesGroup, State


class Receipt(StatesGroup):
    frequency_report = State()
    hours_report = State()

